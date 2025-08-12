from typing import Any
# from django.http import HttpRequest, HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from .models import CustomUser
from django.contrib.auth.decorators import login_required





# class DashboardView(LoginRequiredMixin, TemplateView):
#     template_name = 'dashboard.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user
#         return context
        

# class TimetableListView(LoginRequiredMixin,ListView):
#     model = Timetable
#     template_name = "timetables/timetables_list.html"
#     context_object_name = "timetables"
#     login_url = "login"


# def  get_queryset(self):
#     user = self.request.user
#     # only show timetable matching the user's department
#     return Timetable.objects.filter(department=user.department).order_by('-uploaded_at')
    

# Create your views here.
