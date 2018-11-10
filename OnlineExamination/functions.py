# -*- coding: utf-8 -*-
from django.db.models import Count, Sum
from onlinetest import models
from django.db import connection
import random
import time

def searchmatchuser(username,pwd,useridentity):
    errormsg=""
    if useridentity=="admin" or useridentity=="Admin" or useridentity=="Administrator":
        if models.Admin.objects.filter(username=username).exists():
            userset=models.Admin.objects.get(username=username)
            if userset.pwd==pwd:
                return True,errormsg
            else:
                errormsg="Password wrong!"
                return False,errormsg
        else:
            errormsg="No such user!"
            return False,errormsg

    elif useridentity=="Student" or useridentity=="student":
        if models.Student.objects.filter(username=username).exists():
            userset=models.Student.objects.get(username=username)
            if userset.pwd==pwd:
                return True,errormsg
            else:
                errormsg="Password wrong!"
                return False,errormsg
        else:
            errormsg="No such user!"
            return False,errormsg

    elif useridentity=="Teacher" or useridentity=="teacher":
        if models.Teacher.objects.filter(username=username).exists():
            userset=models.Teacher.objects.get(username=username)
            if userset.pwd==pwd:
                return True,errormsg
            else:
                errormsg="Password wrong!"
                return False,errormsg
        else:
            errormsg="No such user!"
            return False,errormsg

    else:
        errormsg="Unknown Error"
        return False,errormsg

def getadmininfo(username):
    userset=models.Admin.objects.get(username=username)
    return userset

def getstudentinfo(username):
    userset=models.Student.objects.get(username=username)
    return userset

def getteacherinfo(username):
    userset=models.Teacher.objects.get(username=username)
    return userset

def calpapergrade(paperid):
    scores=0
    papercontent=models.Paper_Content.objects.filter(paperid_id=paperid)
    for item in papercontent:
        scores=scores+item.score
    return scores

def runsql(sql):
    cursor=connection.cursor()
    cursor.execute(sql)
    ans=cursor.fetchall()
    return ans

def deluserrecord(form,username):
    if form=="admin" or form=="Admin":
        temprecord = models.Admin.objects.get(username=username)
    elif form=="Student" or form=="student":
        temprecord = models.Student.objects.get(username=username)
    elif form=="Teacher" or form=="teacher":
        temprecord = models.Teacher.objects.get(username=username)
    else:
        print("form error!")
        return False
    temprecord.flag=False
    temprecord.save()
    return True


def delqbrecord(questionid):
    temprecord = models.QuestionBank.objects.get(questionid=questionid)
    temprecord.flag=False
    temprecord.save()
    return True


def delsubjectrecord(subjectid):
    temprecord = models.Subject.objects.get(subjectid=subjectid)
    if temprecord.flag==False:
        temprecord.flag=True
    if  temprecord.flag==True:
        temprecord.flag=False
    temprecord.save()
    return True

def addsubjectrecord(subjectid,name):
    if models.Subject.objects.filter(subjectid=subjectid).exists():
        return False,"record exists!"
    temprecord = models.Subject.objects.create(subjectid=subjectid,name=name)
    temprecord.save()
    return True,""

def addqbrecord(content,answer,choice,score,subject):
    subjectobj = models.Subject.objects.get(name=subject)
    temprecord = models.QuestionBank.objects.create(content=content,answer=answer,choice=choice,score=score,subjectid_id=str(subjectobj.subjectid))
    temprecord.save()
    return True,""

def adduserrecord(form,username,name,pwd,email,major):
    
    if form=="admin" or form=="Admin":
        if models.Admin.objects.filter(username=username).exists():
            return False,"record exists!"
        temprecord = models.Admin.objects.create(username=username,pwd=pwd,name=name,mail=email,major=major)
    elif form=="Student" or form=="student":
        if models.Student.objects.filter(username=username).exists():
            return False,"record exists!"
        temprecord = models.Student.objects.create(username=username,pwd=pwd,name=name,mail=email,major=major)
    elif form=="Teacher" or form=="teacher":
        if models.Teacher.objects.filter(username=username).exists():
            return False,"record exists!"
        temprecord = models.Teacher.objects.create(username=username,pwd=pwd,name=name,mail=email,major=major)
    else:
        print("form error!")
        return False,"no such form!"
    
    temprecord.save()
    return True,""

# temporary rule is random 3 from qb
def makepaper(username,subjectid):
    # generate paperinfo
    date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    paperinfo=models.PaperInfo.objects.create(date=date,subjectid_id=subjectid,studentid_id=username,semester=1)
    paperinfo.save()
    
    # generate papercontent
    maxrecord=models.QuestionBank.objects.filter(flag=True).latest('questionid')
    maxid=maxrecord.questionid

    questionlist=[]
    while len(questionlist)<3:
        questionid=random.randint(1, maxid)
        tempquestionid=models.QuestionBank.objects.get(flag=True,questionid=questionid)
        if tempquestionid.subjectid_id==subjectid:
            if questionid not in questionlist: 
                    questionlist.append(questionid)
                    papercontent=models.Paper_Content.objects.create(paperid_id=paperinfo.paperid,questionid_id=questionid)
                    papercontent.save()

    return paperinfo

def saveanswers(paperid,questionid,answer,ischoice):
    if ischoice=='0':
        questionobj=models.Paper_Content.objects.get(paperid_id=paperid,questionid_id=questionid,flag=True)
        questionobj.answer=answer
        if answer=="":
            questionobj.score=0
        questionobj.save()
        return "success"
    elif ischoice=="1":
        answer=answer.split(')')[1]
        questionobj=models.Paper_Content.objects.get(paperid_id=paperid,questionid_id=questionid,flag=True)
        questionobj.answer=answer
        
        questionbankobj=models.QuestionBank.objects.get(questionid=questionid)
        if questionbankobj.answer==answer:
            questionobj.score=questionbankobj.score
        else:
            questionobj.score=0
        questionobj.save()
        return "success"
    else:
        return "error ischoice val error"

def getteachersubjects(username):
    subjectset=models.Subject_Teacher.objects.filter(teachername_id=username,flag=True)
    subjectidlist=list()
    subjectnamelist=list()
    for item in subjectset:
        subjectidlist.append(item.subjectid_id)\
    # dk

def updatescore(paperid,questionid,score):
    tempobj=models.Paper_Content.objects.get(paperid_id=paperid,questionid_id=questionid,flag=True)
    tempobj.score=score
    tempobj.save()
    return "success"