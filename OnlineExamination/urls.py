"""OnlineExamination URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import view,studentview,adminview,teacherview

urlpatterns = [
    # login pages
    url(r'^main/$', view.main),
    url(r'^login/$', view.loginpage),
    url(r'^logout/$', view.logout),

    url(r'^admin_main$', adminview.admin_main),
    url(r'^student_main$', studentview.student_main),
    url(r'^teacher_main$', teacherview.teacher_main),
    

    # function page 
    
    url(r'^infoeditor/$', adminview.infoeditor),
    url(r'^infoeditor_teacher/$', adminview.infoeditor_teacher),
    url(r'^infoeditor_grade/$', adminview.infoeditor_grade),
    url(r'^questionbank/$', adminview.questionbank),
    url(r'^settings$', adminview.settings),
    url(r'^admininfo/$', adminview.admininfo),

    url(r'^tgradetable$', teacherview.tgradetable),
    url(r'^teachersubjects$', teacherview.teachersubjects),
    url(r'^judgepaper$', teacherview.judgepaper),
    url(r'^teacherinfo$', teacherview.teacherinfo),

    url(r'^personalgrade/$', studentview.personalgrade),
    url(r'^testui/$', studentview.testui),
    url(r'^studentinfo$', studentview.studentinfo),

    url(r'^starttest/$', studentview.starttest),
    url(r'^submitanswer/$', studentview.submitanswer),

    url(r'^startjudgepaper/$', teacherview.startjudgepaper),
    url(r'^submitscore/$', teacherview.submitscore),
    
    # data requests

    url(r'^asset_show_table_student$',view.show_table_student), 
    url(r'^asset_show_table_teacher$',view.show_table_teacher),
    url(r'^asset_show_table_grade$',view.show_table_grade),
    url(r'^asset_show_table_questionbank$',view.asset_show_table_questionbank),
    url(r'^asset_show_table_subject$',view.asset_show_table_subject),
    url(r'^aothertableview/$',view.aothertableview),
    url(r'^studentgrade/$',view.studentgrade),
    
    # db manage solt

    url(r'^databasetest/$',view.databasetest),
    url(r'^btnaddrequest/$',view.btnaddrequest),
    url(r'^btndeleterequest/$',view.btndeleterequest),
    url(r'^btneditrequest/$',view.btneditrequest),
    url(r'^btndeletesubjectrequest/$',view.btndeletesubjectrequest),
    url(r'^btnaddsubjectrequest/$',view.btnaddsubjectrequest),

    url(r'^btndeleteqbrequest/$',view.btndeleteqbrequest),
    url(r'^btnaddqbrequest/$',view.btnaddqbrequest),

    # function test
    url(r'^makepapertest/$', studentview.makepapertest),
    url(r'^setsubjectcookie/$', studentview.setsubjectcookie),
    url(r'^testsubmit$', view.testsubmit),
]