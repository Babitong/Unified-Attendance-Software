from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
# from django.http import HttpRequest 
from .models import CustomUser, Department
from django.contrib.admin import AdminSite
from .models import Timetable
from attendance.models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('date','user', 'scanned_at', 'checked_out_at','latitude','longitude')
    list_filter = ('user__department', 'scanned_at','date')
    search_fields = ('user__username',)
    readonly_fields = ('user', 'scanned_at', 'checked_out_at','latitude','longitude')



class MyAdminSite(AdminSite):
    site_header = 'UNIFIED ADMINISTRATOR DASHBOARD'
    site_title = 'ADMINISTRATOR PORTAL'
    index_title = 'Welcome UNIFIED ADMIN'

    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
        list_display =('name',)
        search_fields = ('name',)

# registering timetable
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
     list_display = ('title','department','uploaded_at')
     fields = ('title','department','upload')
     list_filter = ('department',)
     search_fields = ('title',)
     readonly_fields = ('uploaded_at',)
    

# creating our class for creating users
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'phone_number','department','is_staff')
    fieldsets = UserAdmin.fieldsets+(

        (None, {'fields':('user_type','phone_number','department')}),
        
    ) # type: ignore

    add_fieldsets = UserAdmin.add_fieldsets+(

        (None, {'fields':('user_type','phone_number','department')}),

    )

    # show these fields in the list view
    list_display = ('username','email','user_type','phone_number','department')

    # filter base on role, department, or staff status
    list_filter = ('user_type','department','is_staff')

    # search by username, email,phone number
    search_fields = ('username','email','phone_number')
    ordering = ('user_type','department')
    fieldsets = UserAdmin.fieldsets+(
        ('User Details',{
            'fields':('user_type','phone_number','department'),
        }),
    )  # type: ignore

    # show those same fields when adding users
    add_fieldsets = UserAdmin.add_fieldsets+(
        ('User Details',{
            'fields':('user_type','phone_number','email','department'),
        }),
    )  # type: ignore





admin_site = MyAdminSite(name='myadmin')
admin_site.register(CustomUser,CustomUserAdmin)
admin_site.register(AttendanceRecord, AttendanceRecordAdmin)
admin_site.register(Department,DepartmentAdmin) 
admin_site.register(Timetable,TimetableAdmin)






