from time import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.http import HttpResponseForbidden, HttpResponse
from urllib3 import request
from .models import AttendanceRecord 
import math
from django.template.loader import get_template
from xhtml2pdf import pisa
from utils import generate_attendance_chart 
from users.models import Department , CustomUser
from django.utils import timezone
from datetime import time
from django.db.models import Count



def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 #Meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
     
    a = (math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c
 



 #✅ PDF Export View
def export_pdf(request):
    view_mode = request.GET.get("view")
    
    if view_mode == "all":
        logs = AttendanceRecord.objects.all()
        title = "All Attendance Logs"
    else:
        today = timezone.localdate()
        logs = AttendanceRecord.objects.filter(scanned_at__date=today)
        title = f"Attendance Logs - {today.strftime('%B %d, %Y')}"
    
    context = {
        "logs": logs,
        "title": title,
    }
    
    template = get_template("attendance/pdf.html")
    html = template.render(context)
    
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="attendance_logs.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

# employee pdf view

def employee_export(request):
    view_mode = request.GET.get("view")
    
    if view_mode == "all":
        user = request.user
        # logs = AttendanceRecord.objects.all()
        logs = AttendanceRecord.objects.filter(user=user)
        title = "All Attendance Logs"
    else:
        today = timezone.now()
        logs = AttendanceRecord.objects.filter(user=request.user, scanned_at__date=today)
        title = f"Attendance Logs - {today.strftime('%B %d, %Y')}"
    
    context = {
        "logs": logs,
        "title": title,
    }
    
    template = get_template("attendance/employee_export.html")
    html = template.render(context)
    
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="attendance_logs.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response




@login_required
def post_login_redirect(request):
    user = request.user
     # CHECK FIRST LOGIN
    if user.user_type in ['employee','secretary'] and user.is_first_login:
        return redirect("change_password")
    # NORMAL REDIRECTION
    if user.user_type == "employee":
        return redirect("employee_dashboard")
    elif user.user_type == "secretary":
        return redirect("secretary_dashboard")
    else:
        return redirect("admin:index")
    

@login_required
def change_password(request):
    
    if CustomUser.user_type == "admin": # type: ignore
        return redirect("admin:index")
    if request.method == 'POST': 
        new_password = request.POST.get('password')
        user = request.user
        user.set_password(new_password)
        user.is_first_login = False
        user.save()

        update_session_auth_hash(request, user)
        return redirect('post_login_redirect')
    return render(request,'registration/change_password.html')
    



# Check-in Attendance View

@login_required
def check_in_view(request):
    WORK_START = time(8, 0)
    WORK_END = time(17, 0)
    LATE_THRESHOLD = time(8, 30)

    
    code = request.GET.get('code')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    # Validate QR first
    if code != "http://127.0.0.1:8000/check-in/":
        return HttpResponse("❌ Invalid QR Code")

    # Ensure GPS exists
    if not lat or not lon:
        return HttpResponse("❌ GPS required")

    try:
        user_lat = float(lat)
        user_lon = float(lon)
    except:
        return HttpResponse("❌ Invalid GPS data")

    # Calculate distance
    COMPANY_LAT = user_lat
    COMPANY_LON = user_lon
    ALLOWED_RADIUS = 150 # METERS
    distance = calculate_distance(
        user_lat, user_lon,
        COMPANY_LAT, COMPANY_LON
    )

    # Reject if outside
    if distance > ALLOWED_RADIUS:
        return HttpResponse("❌ You are outside company location")
    


    # Continue attendance logic

    user = request.user
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()
    record = AttendanceRecord.objects.filter(
        user=user,
        date=today
    ).first()

    
    # BEFORE WORK HOURS
    
    if current_time < WORK_START:
        return HttpResponse("❌ Too early to check in")

    
    # AFTER WORK HOURS (NO CHECK-IN)
    
    if current_time > WORK_END and not record:
        return HttpResponse("❌ Work hours closed")

    # CHECK-IN
    if not record:

        if current_time > LATE_THRESHOLD:
            
            status = "Late"
        else:
            status = "Present"
           
        AttendanceRecord.objects.create(
            user=user,
            date=today,
            scanned_at=now,
            status=status,
            latitude=user_lat,
            longitude=user_lon
        )

        # return HttpResponse(f"✅ Checked in ({status})")
        return redirect("scan_checked_in")

   
    # BLOCK MULTIPLE SCANS BEFORE CLOSING
    if record and not record.checked_out_at and current_time < WORK_END:
        return redirect("scan_wait_for_checkout")
        


    # CHECK-OUT (AFTER CLOSING)
    
    if record and not record.checked_out_at and current_time >= WORK_END:

        record.checked_out_at = now
        record.latitude = user_lat
        record.longitude = user_lon
        record.save()

        return redirect("scan_checked_out")

    
    #  FINAL BLOCK
    
    return redirect("scan_already_checked_out")

    



@login_required
def check_in(request):
    return render(request, "attendance/check_in.html")

@login_required
def checked_in_page(request):
    return render(request, "attendance/scan_checked_in.html")

@login_required
def checked_out_page(request):
    return render(request,"attendance/scan_checked_out.html")

@login_required
def wait_for_checkout_page(request):
    return render(request, "attendance/scan_wait_for_checkout.html")

@login_required
def already_checked_out_page(request):
    return render(request, "attendance/scan_already_checked_out.html")


# secretary's dashboard view

@login_required
def secretary_dashboard(request):
    if request.user.user_type.lower() != "secretary":
        return HttpResponseForbidden("Access denied.")
    employees = CustomUser.objects.filter(user_type ='employee')
    # today = now().date()
    today = timezone.now()
    status_list  = []
    for employee in employees:
        records_today = AttendanceRecord.objects.filter( user=employee, date=today)
        if records_today.filter(status='chech_out_at').exists():
            status = 'Checked Out'
        elif records_today.filter(status='scanned_at').exists():
            status = 'Checked In'
        else:
            status = 'Nothing'
        status_list.append({
            'name': employee.get_full_name,
            'department': employee.department,
            'email': employee.email,
            'phone_number': employee.phone_number,
            'status':status,
        })
    # present check
    
    present_check_id = AttendanceRecord.objects.filter(date=today).values_list('user_id', flat=True)
    present_count = employees.filter(id__in=present_check_id).count()

    # absent check
    absent_count = employees.exclude(id__in=present_check_id).count()

    # Total number of teachers
    employee_count = CustomUser.objects.filter(user_type='employee').count()
    
    return render(request, "attendance/secretary_dashboard.html", {
        
        "teacher_count": employee_count,
        "employee": employees,
        "present_count": present_count,
        "absent_count": absent_count,
        "status_list": status_list,


        }) 


# employee dashboard view
        
    
@login_required
def employee_dashboard(request):
    # check if the user clicked "show all records"
    if request.user.user_type.lower() != "employee".lower():
        return HttpResponseForbidden("Access denied.")
    show_all = request.GET.get("view") == "all"
    if show_all:
            records = AttendanceRecord.objects.filter(user=request.user).order_by('-date', '-scanned_at')
            today_label = "All Attendance Records"
            
            
            

    else:
            user = request.user
            # get today's date
            today = timezone.now()
            records = AttendanceRecord.objects.filter(user=user,date=today).order_by('scanned_at')
            today_label = today.strftime("%A, %d %B %Y")
            
        
    return render(request, "attendance/employee_dashboard.html", {
            "records": records,
            "today": today_label,
            "show_all": show_all,
            
            })

def download_qr_page(request):
    qr_path = "/media/qrcodes/general_qrcode.png"
    return render(request, "attendance/qrcode_download.html", {"qr_path":qr_path})


@login_required
def report_view(request):
     # check if the user clicked "show all records"
    show_all = request.GET.get("view") == "all"
    if show_all:
        records = AttendanceRecord.objects.select_related('user').order_by('-date', '-scanned_at')
        today_label = "All Attendance Records"

    else:
        today = timezone.now()
        records = AttendanceRecord.objects.filter(date=today).select_related('user')
        today_label = today.strftime("%A, %d %B %Y")

    # Generate attendance chart data
    attendance_data = (
        records
        .values('user__username')
        .annotate(count=Count('date', distinct=True))
        .order_by('-count')
    )
    # Format data for the chart
    formatted_data = [{"user":entry['user__username'], "count": entry['count']} for entry in attendance_data]
    # Generate the chart
    chart_base64 = generate_attendance_chart(formatted_data)



    return render(request, "report_view.html", {
        "records": records,
        "today": today_label,
        "show_all": show_all,
        "chart_base64": chart_base64,
        }) 
   
    


    























