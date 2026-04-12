from typing import Any
# from django.http import HttpRequest, HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from .models import CustomUser
from django.contrib.auth.decorators import login_required



