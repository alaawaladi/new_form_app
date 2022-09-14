from urllib import response
from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
# def ISP_Email(request) :
#     # return render(request,"home.html")
#     response = redirect('home/')
#     return response


def home(request):
    return render(request,'home.html')

def sent(request):
    return render(request,'sent.html')

def spam(request) :
    return render(request,'spam.html')

def trash(request) :
    return render(request,'trash.html')

def starred(request) :
    return render(request,'starred.html')
