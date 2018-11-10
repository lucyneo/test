from django.http import HttpResponse
from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum

from onlinetest import models
from django.http import JsonResponse
import json
from . import functions 


def admin_main(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getadmininfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('admin-main.html',ctx)
    return response

def infoeditor(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getadmininfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('infoeditor.html',ctx)
    return response

def infoeditor_teacher(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getadmininfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('infoeditor-teacher.html',ctx)
    return response


def infoeditor_grade(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getadmininfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('infoeditor-grade.html',ctx)
    return response


def questionbank(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getadmininfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('questionbankpage.html',ctx)
    return response

def settings(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getadmininfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('settings.html',ctx)
    return response

def admininfo(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getadmininfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('admininfo.html',ctx)
    return response