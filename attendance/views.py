from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponse
from .models import AttendanceRecord 
from users import models
from datetime import timedelta, datetime
from django.template.loader import get_template
from xhtml2pdf import pisa
from Unified_ATTENDANCE_SYSTEM.utils import generate_attendance_chart 
from users.models import Department , CustomUser
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from django.db.models import Count



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



# Redirect after login based on user type
# @login_required
def register_view(request):
    
    departments =  Department.objects.all()
     # Check if an admin already exists
    admin_exists = CustomUser.objects.filter(user_type='admin').exists()

    # Dynamically set the user type based on the existence of an admin
    if admin_exists:
        user_type_choices = [('teacher', 'Teacher'), ('secretary', 'Secretary')]
    else:
        user_type_choices = [('admin', 'Admin'), ('teacher', 'Teacher'), ('secretary', 'Secretary')]

    # getting user data
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        phone_number= request.POST.get('phone_number')
        department_id = request.POST.get('department')
        password = request.POST.get('password')


        # check for existing username or email
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request,"username already exists.")
            return render(request, 'registration/register.html', {'departments': departments})
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,"Email already exists.")
            return render(request, 'registration/register.html', {'departments': departments})
        
        # Get department object
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            messages.error(request, "Invalid department selected.")
            return render(request , 'registration/register.html', {'departments': departments}) 

        # creating user

        CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=user_type,
            phone_number=phone_number,
            department=department,
            password=make_password(password) # Encrypt password
        )  
        messages.success(request, "Account created successfully! You can now login")
        return redirect('login')
        
    return render(request,'registration/register.html', {'departments': departments, 'user_type_choices': user_type_choices})


@login_required
def post_login_redirect(request):
    if request.user.user_type == "teacher":
        return redirect("teacher_home")
    elif request.user.user_type == "secretary":
        return redirect("daily_logs")
    else:
        return redirect("admin:index")
    



# Check-in View

@login_required
def check_in_view(request):
    user = request.user
    now = timezone.localtime()
    today = now.date()

    try:
        record = AttendanceRecord.objects.get(user=user, date=today)
        time_elapsed = (now - record.scanned_at).total_seconds()

        if record.checked_out_at:
            return redirect("scan_already_checked_out")
        # elif time_elapsed >= 4 * 3600: # 4 hours in seconds originally
        elif time_elapsed >= 5 * 60:
            record.checked_out_at = now
            record.save()
            return redirect("scan_checked_out")
        else:
            # remaining = 4 * 3600 - time_elapsed
            return redirect("scan_wait_for_checkout")
    except AttendanceRecord.DoesNotExist:
        AttendanceRecord.objects.create(user=user, scanned_at=now, date=today)
        return redirect( "scan_checked_in")




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


@login_required
def daily_logs(request):
    if request.user.user_type.lower() != "secretary":
        return HttpResponseForbidden("Access denied.")
    
        # return render(request, )
    
    
    
    # check if the user clicked "show all records"
    show_all = request.GET.get("view") == "all"
    if show_all:
        records = AttendanceRecord.objects.select_related('user').order_by('-date', '-scanned_at')
        today_label = "All Attendance Records"

    else:
        today = timezone.localdate()
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

    # Total number of teachers
    teacher_count = CustomUser.objects.filter(user_type='teacher').count()



    return render(request, "attendance/daily_logs.html", {
            "records": records,
        "today": today_label,
        "show_all": show_all,
        "chart_base64": chart_base64,
        "teacher_count": teacher_count,
        }) 
        # date_str = request.GET.get("date")
        # records = AttendanceRecord.objects.all().order_by("scanned_at")

        # if date_str:
        #     try:
        #         filter_date = timezone.datetime.strptime(date_str,"%Y-%m-%d").date()
        #         records = records.filter(scanned_at__date=filter_date)
        #     except ValueError:
        #         pass
        # return render(request,"attendance/daily_logs.html",{"records": records, "scanned_date": date_str})
    
@login_required
def teacher_home_view(request):

     
    # check if the user clicked "show all records"
    show_all = request.GET.get("view") == "all"
    if show_all:
        records = AttendanceRecord.objects.filter(user=request.user).order_by('-date', '-scanned_at')
        today_label = "All Attendance Records"
        
        

    else:
        today = timezone.localdate()
        records = AttendanceRecord.objects.filter(date=today).select_related('user')
        today_label = today.strftime("%A, %d %B %Y")
        
        
    return render(request, "attendance/teacher_home.html", {
            "records": records,
        "today": today_label,
        "show_all": show_all,
        
        })

def download_qr_page(request):
    qr_path = "/media/qrcodes/general_qrcode.png"
    return render(request, "attendance/qrcode_download.html", {"qr_path":qr_path})


@login_required
def dashboard_view(request):
     # check if the user clicked "show all records"
    show_all = request.GET.get("view") == "all"
    if show_all:
        records = AttendanceRecord.objects.select_related('user').order_by('-date', '-scanned_at')
        today_label = "All Attendance Records"

    else:
        today = timezone.localdate()
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



    return render(request, "dashboard.html", {
            "records": records,
        "today": today_label,
        "show_all": show_all,
        "chart_base64": chart_base64,
        }) 
   
    

# Secretary Dashboard charts and statistics




















