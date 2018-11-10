# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum
from django.core.exceptions import ObjectDoesNotExist
from onlinetest import models
from django.http import JsonResponse
import json
from . import functions
from django.core.paginator import Paginator,InvalidPage,EmptyPage

from django.db import connection
cursor=connection.cursor()

def main(request):
    # context = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'main.html')

def loginpage(request):
    ctx ={}
    if request.method=='GET':
        ctx['error']=0
        return render(request,'login.html',ctx)
    if request.method=='POST' and 'login' in request.POST:
        
        if request.POST:
            username= request.POST['inputUsername']
            pwd=request.POST['inputPassword']
            useridentity=request.POST['selectid']
        print(useridentity)
        flag,errormsg=functions.searchmatchuser(username,pwd,useridentity)

        if flag:
            if useridentity=="Administrator":
                userinfo=functions.getadmininfo(username)
                # print(userinfo.name,userinfo.mail)
                ctx['username']=userinfo.username
                ctx['name']=userinfo.name
                ctx['pwd']=userinfo.pwd
                ctx['mail']=userinfo.mail
                response=render_to_response('admin-main.html',ctx)
                response.set_cookie("userid",username)
                return response
            elif useridentity=="Student":
                userinfo=functions.getstudentinfo(username)
                # print(userinfo.name,userinfo.mail)
                ctx['username']=userinfo.username
                ctx['name']=userinfo.name
                ctx['pwd']=userinfo.pwd
                ctx['mail']=userinfo.mail
                response=render_to_response('student-main.html',ctx)
                response.set_cookie("userid",username)
                return response
            elif useridentity=="Teacher":
                userinfo=functions.getteacherinfo(username)
                # print(userinfo.name,userinfo.mail)
                ctx['username']=userinfo.username
                ctx['name']=userinfo.name
                ctx['pwd']=userinfo.pwd
                ctx['mail']=userinfo.mail
                response=render_to_response('teacher-main.html',ctx)
                response.set_cookie("userid",username)
                return response
            else:
                ctx['error']=1
                ctx['errormsg']="Unknown Error"
                return render(request,'login.html',ctx)
                
        else:
            ctx['error']=1
            ctx['errormsg']=errormsg
            return render(request,'login.html',ctx)
    else:
        ctx['error']=1
        ctx['errormsg']="Unknown Error"
        return render(request,'login.html',ctx)
    

def logout(request):
    ctx={}
    ctx['success']=1
    response=render_to_response('main.html',ctx)
    response.delete_cookie('userid')
    return response




def aothertableview(request):
    qs = models.Admin.objects.all()  # Use the Pandas Manager
    df = qs
    template = 'infoeditor.html'
    #Format the column headers for the Bootstrap table, they're just a list of field names, 
    #duplicated and turned into dicts like this: {'field': 'foo', 'title: 'foo'}
    columns = [{'field': "username", 'title': "username"},{'field': "name", 'title': "name"},{'field': "pwd", 'title': "pwd"},{'field': "mail", 'title': "mail"}]
    #Write the DataFrame to JSON (as easy as can be)
    json = df # output just the records (no fieldnames) as a collection of tuples
    #Proceed to create your context object containing the columns and the data
    context = {
                'data': json,
                'columns': columns
                }
    #And render it!
    # print(context)
    return render(request, template, context)

def show_table_student(request):

    if request.method == "GET":
        print(request.GET)
        limit = request.GET.get('limit')   # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        search = request.GET.get('search')
        sort_column = request.GET.get('ordername')   # which column need to sort
        order = request.GET.get('order')    # ascending or descending
        # search=search.encode('utf8')
        print(order)
        print(sort_column)
        # searchkey=request.GET['username']
        if search:    
            all_records = models.Student.objects.filter(username=str(search),flag=True)
        else:
            all_records = models.Student.objects.filter(flag=True)
        
        if sort_column:
            if sort_column=="username":
                if order == 'desc':
                    all_records = models.Student.objects.filter(flag=True).order_by(sort_column)
        


        # if sort_column:   # 判断是否有排序需求
        #     sort_column = sort_column.replace('asset_', '')    
        #     if sort_column in ['id','asset_type','sn','name','management_ip','manufactory','type']:   # 如果排序的列表在这些内容里面
        #         if order == 'desc':   # 如果排序是反向
        #             sort_column = '-%s' % (sort_column)
        #         all_records = models.Asset.objects.all().order_by(sort_column)
        #     elif sort_column in ['salt_minion_id','os_release',]:
        #         # server__ 表示asset下的外键关联的表server下面的os_release或者其他的字段进行排序
        #         sort_column = "server__%s" % (sort_column)
        #         if order == 'desc':
        #             sort_column = '-%s'%(sort_column)
        #         all_records = models.Asset.objects.all().order_by(sort_column)
        #     elif sort_column in ['cpu_model','cpu_count','cpu_core_count']:
        #         sort_column = "cpu__%s" %(sort_column)
        #         if order == 'desc':
        #             sort_column = '-%s'%(sort_column)
        #         all_records = models.Asset.objects.all().order_by(sort_column)
        #     elif sort_column in ['rams_size',]:
        #         if order == 'desc':
        #             sort_column = '-rams_size'
        #         else:
        #             sort_column = 'rams_size'
        #         all_records = models.Asset.objects.all().annotate(rams_size = Sum('ram__capacity')).order_by(sort_column)
        #     elif sort_column in ['localdisks_size',]:  # using variable of localdisks_size because there have a annotation below of this line
        #         if order == "desc":
        #             sort_column = '-localdisks_size'
        #         else:
        #             sort_column = 'localdisks_size'
        #         #     annotate 是注释的功能,localdisks_size前端传过来的是这个值，后端也必须这样写，Sum方法是django里面的，不是小写的sum方法，
        #         # 两者的区别需要注意，Sum（'disk__capacity‘）表示对disk表下面的capacity进行加法计算，返回一个总值.
        #         all_records = models.Asset.objects.all().annotate(localdisks_size=Sum('disk__capacity')).order_by(sort_column)   

        #     elif sort_column in ['idc',]:
        #         sort_column = "idc__%s" % (sort_column)
        #         if order == 'desc':
        #             sort_column = '-%s'%(sort_column)
        #         all_records = models.Asset.objects.all().order_by(sort_column)

        #     elif sort_column in ['trade_date','create_date']:
        #         if order == 'desc':
        #             sort_column = '-%s'%sort_column
        #         all_records = models.Asset.objects.all().order_by(sort_column)
            


        all_records_count=all_records.count()

        if not offset:
            offset = 0
        if not limit:
            limit = 20    

        pageinator = Paginator(all_records, limit)   # 开始做分页
        page = int(int(offset) / int(limit) + 1)    
        response_data = {'total':all_records_count,'rows':[]}   

        # response_data['rows']=all_records
        for asset in pageinator.page(page):
            if asset.flag:
                response_data['rows'].append({
                    "username": asset.username,   
                    "name" : asset.name,
                    "pwd":asset.pwd,
                    "mail":asset.mail,
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                })
        return JsonResponse(response_data)




def show_table_teacher(request):
    
    if request.method == "GET":
        print(request.GET)
        limit = request.GET.get('limit')   # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        search = request.GET.get('search')
        sort_column = request.GET.get('ordername')   # which column need to sort
        order = request.GET.get('order')      # ascending or descending
        
        if search:    #    
            all_records = models.Teacher.objects.filter(username=str(search),flag=True)
        else:
            all_records = models.Teacher.objects.filter(flag=True)   # must be wirte the line code here
        print(sort_column)
        if sort_column:
            if sort_column=="username":
                if order == 'desc':
                    all_records = models.Teacher.objects.filter(flag=True).order_by(sort_column)
                    
        all_records_count=all_records.count()

        if not offset:
            offset = 0
        if not limit:
            limit = 20   

        pageinator = Paginator(all_records, limit)   # 开始做分页 

        page = int(int(offset) / int(limit) + 1)    
        response_data = {'total':all_records_count,'rows':[]}   
        for asset in pageinator.page(page):    
            response_data['rows'].append({
                "username": asset.username,   
                "name" : asset.name,
                "pwd":asset.pwd,
                "mail":asset.mail,
            })

        return JsonResponse(response_data)

def show_table_grade(request):
    if request.method == "GET":
        username=request.COOKIES['userid']
        print(request.GET)
        limit = request.GET.get('limit')   # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        search = request.GET.get('search')
        sort_column = request.GET.get('ordername')   # which column need to sort
        order = request.GET.get('order')      # ascending or descending
        
        sql='''select  onlinetest_paperinfo.paperid,onlinetest_student.username,onlinetest_student.name,onlinetest_subject.name,onlinetest_paperinfo.date,sum(onlinetest_paper_content.score)
        from onlinetest_paperinfo,onlinetest_paper_content,onlinetest_subject,onlinetest_student
        where onlinetest_paperinfo.subjectid_id=onlinetest_subject.subjectid
        and   onlinetest_paper_content.paperid_id=onlinetest_paperinfo.paperid
        and   onlinetest_paperinfo.studentid_id=onlinetest_student.username
        group by onlinetest_paperinfo.paperid
        '''  

        if search:    #    
            sql = '''select  onlinetest_paperinfo.paperid,onlinetest_student.username,onlinetest_student.name,onlinetest_subject.name,onlinetest_paperinfo.date,sum(onlinetest_paper_content.score)
        from onlinetest_paperinfo,onlinetest_paper_content,onlinetest_subject,onlinetest_student
        where onlinetest_paperinfo.subjectid_id=onlinetest_subject.subjectid
        and   onlinetest_paper_content.paperid_id=onlinetest_paperinfo.paperid
        and   onlinetest_paperinfo.studentid_id=onlinetest_student.username
        and   onlinetest_student.username='''+'\''+str(search)+'\''+'''
        group by onlinetest_paperinfo.paperid
        '''  
        

        print(sort_column)
        if sort_column:
            
            if sort_column=="username":
                if order == 'desc':
                    sql=sql+''' order by onlinetest_student.username desc'''

            if sort_column=="paperid":
                if order == 'desc':
                    sql=sql+''' order by  onlinetest_paperinfo.paperid desc'''

            if sort_column=="date":
                if order == 'desc':
                    sql=sql+''' order by  onlinetest_paperinfo.date desc'''

            if sort_column=="grade":
                if order == 'desc':
                    sql=sql+''' order by  sum(onlinetest_paper_content.score) desc'''


        all_records = functions.runsql(sql)   # must be wirte the line code here

        all_records_count=len(all_records)

        if not offset:
            offset = 0
        if not limit:
            limit = 20    
        pageinator = Paginator(all_records, limit)   # 开始做分页

        page = int(int(offset) / int(limit) + 1)    
        response_data = {'total':all_records_count,'rows':[]}   
        for asset in pageinator.page(page):    
            response_data['rows'].append({
                "paperid": asset[0],   
                "username" : asset[1],
                "name":asset[2],
                "subjectname":asset[3],
                "date":asset[4],
                "grade":asset[5],
            })
        return JsonResponse(response_data)



def asset_show_table_questionbank(request):
    if request.method == "GET":
        print(request.GET)
        limit = request.GET.get('limit')   # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        search = request.GET.get('search')
        sort_column = request.GET.get('ordername')   # which column need to sort
        order = request.GET.get('order')      # ascending or descending
        
        sql='''
        select  questionid,content,choice,answer,score,onlinetest_subject.name
        from onlinetest_subject,onlinetest_questionbank
        where onlinetest_questionbank.subjectid_id=onlinetest_subject.subjectid
        and   onlinetest_questionbank.flag=1
        order by questionid
        '''   
        print(search)
        if search: 
             sql='''
        select  questionid,content,choice,answer,score,onlinetest_subject.name
        from onlinetest_subject,onlinetest_questionbank
        where onlinetest_questionbank.subjectid_id=onlinetest_subject.subjectid
        and   onlinetest_questionbank.flag=1
        and   questionid='''+str(search)


        all_records = functions.runsql(sql)   # must be wirte the line code here

        all_records_count=len(all_records)

        if not offset:
            offset = 0
        if not limit:
            limit = 20    
        pageinator = Paginator(all_records, limit)   # 开始做分页

        page = int(int(offset) / int(limit) + 1)    
        response_data = {'total':all_records_count,'rows':[]}   
        for asset in pageinator.page(page):    
            response_data['rows'].append({
                "questionid": asset[0],   
                "content" : asset[1],
                "choice":asset[2],
                "answer":asset[3],
                "score":asset[4],
                "subjectid_id":asset[5],
            })
        return JsonResponse(response_data)

def asset_show_table_subject(request):
   
    if request.method == "GET":
        print(request.GET)
        limit = request.GET.get('limit')   # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        search = request.GET.get('search')
        sort_column = request.GET.get('ordername')   # which column need to sort
        order = request.GET.get('order')      # ascending or descending
        
        if search:    #    
            all_records = models.Subject.objects.filter(subjectid=str(search))
        else:
            all_records = models.Subject.objects.all()   # must be wirte the line code here
        print(sort_column)
        if sort_column:
            if sort_column=="subjectid":
                if order == 'desc':
                    all_records = models.Subject.objects.all().order_by(sort_column)
                    
        all_records_count=all_records.count()

        if not offset:
            offset = 0
        if not limit:
            limit = 20    
        pageinator = Paginator(all_records, limit)   # 开始做分页
        page = int(int(offset) / int(limit) + 1)    
        response_data = {'total':all_records_count,'rows':[]}   
        for asset in pageinator.page(page):    
            response_data['rows'].append({
                "subjectid": asset.subjectid,   
                "name" : asset.name,
                "flag":asset.flag,
            })

        return JsonResponse(response_data)

def studentgrade(request):
    if request.method == "GET":
        username=request.COOKIES['userid']
        print(request.GET)
        limit = request.GET.get('limit')   # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        search = request.GET.get('search')
        sort_column = request.GET.get('ordername')   # which column need to sort
        order = request.GET.get('order')      # ascending or descending
        
        sql='''select  onlinetest_paperinfo.paperid,onlinetest_student.username,onlinetest_student.name,onlinetest_subject.name,onlinetest_paperinfo.date,sum(onlinetest_paper_content.score)
        from onlinetest_paperinfo,onlinetest_paper_content,onlinetest_subject,onlinetest_student
        where onlinetest_paperinfo.subjectid_id=onlinetest_subject.subjectid
        and   onlinetest_paper_content.paperid_id=onlinetest_paperinfo.paperid
        and   onlinetest_paperinfo.studentid_id=onlinetest_student.username
        and   onlinetest_student.username=\''''+username+'\''+'''
        group by onlinetest_paperinfo.paperid
        '''  
        print(sort_column)
        
        if sort_column:
            
            if sort_column=="username":
                if order == 'desc':
                    sql=sql+''' order by onlinetest_student.username desc'''

            if sort_column=="paperid":
                if order == 'desc':
                    sql=sql+''' order by  onlinetest_paperinfo.paperid desc'''

            if sort_column=="date":
                if order == 'desc':
                    sql=sql+''' order by  onlinetest_paperinfo.date desc'''

            if sort_column=="grade":
                if order == 'desc':
                    sql=sql+''' order by  sum(onlinetest_paper_content.score) desc'''



        all_records = functions.runsql(sql)   # must be wirte the line code here

        all_records_count=len(all_records)

        if not offset:
            offset = 0
        if not limit:
            limit = 20    
        pageinator = Paginator(all_records, limit)   # 开始做分页

        page = int(int(offset) / int(limit) + 1)
        response_data = {'total':all_records_count,'rows':[]}   
        for asset in pageinator.page(page):    
            response_data['rows'].append({
                "paperid": asset[0],   
                "username" : asset[1],
                "name":asset[2],
                "subjectname":asset[3],
                "date":asset[4],
                "grade":asset[5],
            })
        return JsonResponse(response_data)


def databasetest(request):
    # grade search ex: (1, u'111', u'zsq', u'math', u'20170709', 10)  datafield problem unsolved
    # sql='''select  onlinetest_paperinfo.paperid,onlinetest_student.username,onlinetest_student.name,onlinetest_subject.name,onlinetest_paperinfo.date,sum(onlinetest_paper_content.score)
    # from onlinetest_paperinfo,onlinetest_paper_content,onlinetest_subject,onlinetest_student
    # where onlinetest_paperinfo.subjectid_id=onlinetest_subject.subjectid
    # and   onlinetest_paper_content.paperid_id=onlinetest_paperinfo.paperid
    # and   onlinetest_paperinfo.studentid_id=onlinetest_student.username
    # group by onlinetest_paperinfo.paperid
    # '''
    subjectname='数学'
    username='E11414026'
    sql=''' select onlinetest_paper_content.paperid_id,onlinetest_paper_content.questionid_id,onlinetest_paper_content.answer
        from onlinetest_paper_content,onlinetest_paperinfo,onlinetest_subject
        where onlinetest_paper_content.paperid_id=onlinetest_paperinfo.paperid
        and   onlinetest_paperinfo.subjectid_id=onlinetest_subject.subjectid
        and   onlinetest_subject.name='''+'\''+subjectname+'\''+'''
        and   onlinetest_paperinfo.studentid_id='''+'\''+username+'\''

    ans=functions.runsql(sql)
    
    return HttpResponse(ans)


def btndeleterequest(request):
    if request.method=='POST':
        print(request.POST)
        ids=[]
        form=request.POST.get('form')
        ids=request.POST.getlist('usersets[]')
        for username in ids:
            if functions.deluserrecord(form,username)==False:
                return HttpResponse('Error！')
        return HttpResponse('success')
        # return JsonResponse("success")


def btnaddqbrequest(request):
    if request.method=='POST':
        print(request.POST)
        
        content=request.POST.get('content')
        answer=request.POST.get('answer')
        score=request.POST.get('score')
        subject=request.POST.get('subject')
        choice=request.POST.get('choice')

        flag,msg=functions.addqbrecord(content,answer,choice,score,subject)
        if flag==False:
            return HttpResponse('Error:'+msg)
        else:
            return HttpResponse('success')


def btndeleteqbrequest(request):
    if request.method=='POST':
        print(request.POST)
        ids=[]
 
        ids=request.POST.getlist('questionidset[]')
        for questionid in ids:
            if functions.delqbrecord(questionid)==False:
                return HttpResponse('Error！')
        return HttpResponse('success')
        # return JsonResponse("success")

def btndeletesubjectrequest(request):
    if request.method=='POST':
        print(request.POST)
        ids=[]
        ids=request.POST.getlist('subjectsets[]')
        print(ids)
        for subjectid in ids:
            if functions.delsubjectrecord(subjectid)==False:
                return HttpResponse('Error！')
        return HttpResponse('success')
        # return JsonResponse("success")

def btnaddsubjectrequest(request):
    if request.method=='POST':
        print(request.POST)
        
        subjectid=request.POST.get('subjectid')
        name=request.POST.get('name')

        flag,msg=functions.addsubjectrecord(subjectid,name)
        if flag==False:
            return HttpResponse('Error:'+msg)
        else:
            return HttpResponse('success')


def btnaddrequest(request):
    if request.method=='POST':
        print(request.POST)
        
        username=request.POST.get('username')
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        email=request.POST.get('email')
        major=request.POST.get('major')
        form=request.POST.get('form')
        
        flag,msg=functions.adduserrecord(form,username,name,pwd,email,major)
        if flag==False:
            return HttpResponse('Error:'+msg)
        else:
            return HttpResponse('success')

def btneditrequest(request):
    if request.method=='POST':
        print(request.POST)
        ids=[]
        form=request.POST.get('form')
        ids=request.POST.getlist('usersets[]')
        for username in ids:
            print(username)
        
        return HttpResponse('success') 


def testsubmit(request):
    if request.method=='POST':
        print(request.POST)

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
        # return HttpResponse("True") 