from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import json
import main
import re
# Create your views here.
def index(request):
    return render(request, 'gv/index.html')
def get(request):
    stunum=request.POST['stunum']
    p=request.POST['pass']
    URL="https://rs.rikkyo.ac.jp/"
    value=[stunum,p]
    result, list_pie, list_bar, table = main.condact(value)
    #名前の取得
    name = result[0].iloc[2,2]
    #単位の達成率
    get_unit, required_unit = list_pie[6][5:7]
    gradeAchievement = (get_unit / required_unit) * 100
    #GPA
    gpa = list(result[1]['累計'])[-1]
    #単位のリスト
    Achivement_list = list(list_bar[2]['現在達成率(%)'])
    str_Achievement_list = str(Achivement_list)[1:-2]
    kind_name = list(list_bar[2].index)
    str_kind_name = str(kind_name)[1:-2].replace("'","")
    kome = str_kind_name[0]
    str_kind_name = str_kind_name.replace(kome,'')
    str_name = ''
    alnumReg = re.compile(r'^[a-zA-Z0-9]+$')
    def isalnum(s):
        return alnumReg.match(s) is not None
    for i in name:
        if isalnum(i):
            str_name = str_name + i
    #results=main.condact(value)
    #table=main.condact(value)
    #table=table.to_html()
    print(str_Achievement_list)
    params = {
        'gradeAchievement':gradeAchievement,
        'str_Achievement_list':str_Achievement_list,
        'str_kind_name':str_kind_name,
        'name':str_name,
        'gpa':gpa
    }
    #for i, result in enumerate(results):
        #html=result.to_html()
        #key = 'result'+str(i)
        #params[key]=html
    return render(request, 'gv/get.html', params)
