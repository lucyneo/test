from django.http import HttpResponse
from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum

from onlinetest import models
from django.http import JsonResponse
import json
from . import functions 



def teacher_main(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getteacherinfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('teacher-main.html',ctx)
    return response


def tgradetable(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getteacherinfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('tgradetable.html',ctx)
    return response


def teachersubjects(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getteacherinfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('teachersubjects.html',ctx)
    return response


def judgepaper(request):
    
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getteacherinfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail
    
    subjectlist=[]
    sql=''' select onlinetest_subject.name
    from onlinetest_subject,onlinetest_subject_teacher
    where onlinetest_subject.subjectid=onlinetest_subject_teacher.subjectid_id
    and   onlinetest_subject_teacher.flag=1
    and   onlinetest_subject.flag=1
    and   onlinetest_subject_teacher.teachername_id=
    '''
    sql=sql+'\''+userinfo.username+'\''
    result=functions.runsql(sql)
    for item in result:
        subjectlist.append(item[0])  # direct sql item has no attribute in tables
    ctx['subjectlist']=subjectlist
    response=render_to_response('judgepaper.html',ctx)
    return response
    


def startjudgepaper(request):
    if request.method == "POST":
        print(request.POST)
        subjectname = request.POST.get('subjectname') 
        ctx={}
        username=request.COOKIES['userid']
        print(username)
        userinfo=functions.getteacherinfo(username)
        ctx['username']=userinfo.username
        ctx['name']=userinfo.name
        ctx['pwd']=userinfo.pwd
        ctx['mail']=userinfo.mail

        sql=''' select onlinetest_paper_content.paperid_id,onlinetest_paper_content.questionid_id,onlinetest_questionbank.content,onlinetest_paper_content.answer
        from onlinetest_paper_content,onlinetest_paperinfo,onlinetest_subject,onlinetest_questionbank
        where onlinetest_paper_content.paperid_id=onlinetest_paperinfo.paperid
        and   onlinetest_paperinfo.subjectid_id=onlinetest_subject.subjectid
        and   onlinetest_questionbank.questionid=onlinetest_paper_content.questionid_id
        and   onlinetest_subject.name='''+'\''+subjectname+'\''+'''
        and   onlinetest_paper_content.score is null
        '''
        questionlist=functions.runsql(sql)
        result=list()
        i=1
        for item in questionlist:
            questionelement=dict()
            questionelement['num']=i
            questionelement['questionid']=item[1]
            questionelement['content']=item[2]
            questionelement['answer']=item[3]
            questionelement['paperid']=item[0]
            result.append(questionelement)
            i=i+1
        ctx['questionlist']=result

        response=render_to_response('judgepaperfun.html',ctx)
        return response

def teacherinfo(request):
    ctx={}
    username=request.COOKIES['userid']
    print(username)
    userinfo=functions.getteacherinfo(username)
    ctx['username']=userinfo.username
    ctx['name']=userinfo.name
    ctx['pwd']=userinfo.pwd
    ctx['mail']=userinfo.mail        
    response=render_to_response('teacherinfo.html',ctx)
    return response


def submitscore(request):
    if request.method == "POST":
        print(request.POST)
        paperid = request.POST.get('paperid') 
        questionid = request.POST.get('questionid') 
        score = request.POST.get('score') 
        msg=functions.updatescore(paperid,questionid,score)
        return HttpResponse(msg)
    else:
        return HttpResponse("error")