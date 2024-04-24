# views.py

from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the home page!")  # 返回欢迎信息
