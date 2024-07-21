from myapp.api import api
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse



def home(request):
    return HttpResponse("Welcome to the Online Library Management System")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', home),
]
