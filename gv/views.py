from django.shortcuts import render, redirect
#from .forms import userInfoForm, findForm
from .models import studentInfo, subjectInfo
import main
from pytojs import pytojsMaterials
import sys
import traceback
from main import condact

######################################################################################
                #10/01追加
###################################################################################
#from django.shortcuts import render, redirect
from .forms import userInfoForm, findForm, find_my_sub_Form
#from .models import studentInfo, subjectInfo
#from main import condact
#from pytojs import pytojsMaterials
from django.db.models import Q
from django.forms import Select


import time

# Create your views here.


###################################################################################
                                    #トップページ
######################################################################################

def hp(request):
    '''params = {
        'str_name':str_name,
        'gradeAchievement':gradeAchievement
    }'''
    #params3 = params2

    return render(request, 'gv/hp.html')

###################################################################################
                                    #ログイン画面
##################################################################################
def index(request):
    form = userInfoForm()
    index_params = {
        'form':form,
        'message':'学籍番号とパスワードを入力してください',
        }
    time.sleep(2)
    return render(request, 'gv/index.html', index_params)

####################################################################################
                                #ログイン後のメイン画面用
####################################################################################
def mainhome_after_login(request):
    try: #ログインしているか確かめる
        mainhome_after_login = login
        #print(mainhome_after_login)
    except Exception:
        mainhome_after_login = 'no'
    #一度mainhomeに入っていれば実行
    if mainhome_after_login == 'ok':

        time.sleep(2)
        return render(request, 'gv/mainhome.html', mainhome_params)
    else:
        form = userInfoForm()
        index_params = {
            'form':form
        }
        return render(request, 'gv/index.html', index_params)

def get(request):
    if request.method == 'POST':
        #formから学籍番号とパスワードの取得
        value = [request.POST['stunum'], request.POST['password']]
        #入力が正しいか

        try:
            result, list_pie, list_bar, table, personal_dataset= main.condact(value)
        #正しくなかったら戻る
        except:
            form = userInfoForm()
            #error = str(e.args)
            #error = str(sys.exc_info()[-1].tb_lineno)
            error=traceback.format_exc()
            params = {
            'form':form,
            #'message':'学籍番号かパスワードがまちがえてるよ♡<br>\
            #もう一度入力してね♡'
            'message':error
            }
            return render(request, 'gv/index.html', params)


        #result, list_pie, list_bar, table, personal_dataset= main.condact(value)


        #正しくデータを整形することができるかどうか。
        try:
            #pythonからjsへの値の受け渡し
            params = pytojsMaterials(result, list_pie, list_bar, table)


        except Exception as e:
            print("エラーの種類:", e.args)
            form = userInfoForm()
            params = {
            'form':form,
            'message':str(e.args)
            }
            return render(request, 'gv/index.html', params)

        #データベースに登録するかどうか
        stuobj = studentInfo.objects.all()
        t = list(personal_dataset.iloc[0])
        if t[0] not in str(stuobj):
            print('なかったからsaveするよ')
            #user情報の保存
            stuinfo = studentInfo(user_id=t[0], student_grade=t[1],
            enteryear=t[2], seasons=t[3], gpa=t[4])
            stuinfo.save()
            #studentInfo(*t).save()

            #教科情報の保存
            for i in range(len(table)):
                s = list(table.iloc[i])
                subjectInfomation = subjectInfo(subjectnum=s[0],managementnum=s[1],
                user_id=s[2],subjectname=s[3],unit_int=s[4],grade=s[5],
                grade_score_int=s[6],result_score_int=s[7],year_int=s[8],
                season=s[9],teacher=s[10],gpa_int=s[11],
                category1=s[12],category2=s[13],last_login=s[14],stu_id=stuinfo)
                subjectInfomation.save()

        #データベースから情報を取得
        #後々新しいpyファイルを作成する
        #gpaの順位
        gpaobj = studentInfo.objects.filter(gpa__gt = float(params['gpa']))
        rank = len(gpaobj) + 1
        params['rank'] = rank
        return render(request, 'gv/get.html', params)
    else:
        form = userInfoForm()
        params = {
        'form':form,
        'message':'学籍番号とパスワードを入力しよう!'
        }
        return render(request, 'gv/index.html', params)
###################################################################################

######################################################################################


def deteil(request):
    if request.method == 'GET':
        form = findForm()
        params = {
            'form':form,
            'str':'検索してね♡'
        }
        return render(request, 'gv/deteil.html', params)
    else:
        params = {
            'form':findForm(request.POST),
            'str':request.POST['find']
        }
        #data = subjectInfo.objects.all().filter(user_id__contains=params['str'])
        data = subjectInfo.objects.all()

        for i in list(data):
            print(i)

        return render(request, 'gv/deteil.html', params)

######################################################################################
                                     #詳細画面
###################################################################################


def detail(request):
    ###################################################################
        ##直すところ##
    ###############################################################
    try:
        sn = personal_dataset.loc[0,'user_id']   #ログイン中のユーザーの学籍番号
        #sn = '16cb087l'
    #ログインしてからでなければ入れない
    except Exception as e:
        print(str(e.args))
        form = userInfoForm()
        index_params = {
            'form':form
        }
        return render(request, 'gv/index.html', index_params)



    if request.method == 'POST':
        form = find_my_sub_Form(request.POST)


        ######################################################################################################
                                        #yearのフォームを人それぞれで分ける
        ######################################################################################################
        year_list = list(set(list(subjectInfo.objects.filter(user_id=sn).values_list('year_int', flat=True))))
        form = find_my_sub_Form()
        year_field = form.fields['year']
        c = [('','year')]
        for i in range(0, len(year_list)):
            year_tuple = (str(year_list[i]),str(year_list[i]))
            c.append(year_tuple)
        print(c)
        year_field.choices = c
        #year_field.widget = Select(choices=c)
        #form.fields['year'] = year_field
        #orm.full_clean()

        ######################################################################################################
                                #category1のフォームを人それぞれで分ける
        ######################################################################################################
        category1_list = list(set(list(subjectInfo.objects.filter(user_id=sn).values_list('category1', flat=True))))
        print(category1_list)

        category1_field = form.fields['category1']
        c = [('','kind1')]
        for i in range(0, len(category1_list)):
            category1_tuple = (category1_list[i],category1_list[i])
            c.append(category1_tuple)
        category1_field.choices = c










        filtered_sub = subjectInfo.objects.filter(user_id=sn)
        season = request.POST['season']
        grade = request.POST['grade']
        year = request.POST['year']
        category1 = request.POST['category1']
        print(year)
        subname_teacher = request.POST['subname_teacher']

        #今期の成績を選択した場合
        try:
            gv = request.POST['gv']
            form = find_my_sub_Form()
            filtered_sub = filtered_sub.filter(season__contains='春学期').filter(year_int=2018)
            detail_params = {
                'filtered_sub':filtered_sub,
                'form':form
            }

            time.sleep(2)

            return render(request, 'gv/detail.html', detail_params)
        except:
            pass
        #季節のフィルター
        if len(season) is not 0:
            filtered_sub = filtered_sub.filter(season__contains=season)
        #成績のフィルター
        if len(grade) is not 0:
            g = int(grade)
            filtered_sub = filtered_sub.filter(grade_score_int=g)
        #科目名か先生の名前
        if len(subname_teacher) is not 0:
            filtered_sub = filtered_sub.filter(
                Q(subjectname__contains=subname_teacher)|
                Q(teacher__contains=subname_teacher)
                ).distinct()
        #category1のフィルター
        if len(category1) is not 0:
            filtered_sub = filtered_sub.filter(category1=category1)
        #受講年度のフィルター
        if len(year) is not 0:
            y = int(year)
            filtered_sub = filtered_sub.filter(year_int=y)

        detail_params = {
            'filtered_sub':filtered_sub,
            'form':form
        }


        time.sleep(2)



        return render(request, 'gv/detail.html', detail_params)
    else:
        ######################################################################################################
                                        #yearのフォームを人それぞれで分ける
        ######################################################################################################
        year_list = list(set(list(subjectInfo.objects.filter(user_id=sn).values_list('year_int', flat=True))))
        form = find_my_sub_Form()
        year_field = form.fields['year']
        c = [('','year')]
        for i in range(0, len(year_list)):
            year_tuple = (str(year_list[i]),str(year_list[i]))
            c.append(year_tuple)
        year_field.choices = c
        #year_field.widget = Select(choices=c)
        #form.fields['year'] = year_field
        #orm.full_clean()

        ######################################################################################################
                                #category1のフォームを人それぞれで分ける
        ######################################################################################################
        category1_list = list(set(list(subjectInfo.objects.filter(user_id=sn).values_list('category1', flat=True))))


        category1_field = form.fields['category1']
        c = [('','kind1')]
        for i in range(0, len(category1_list)):
            category1_tuple = (category1_list[i],category1_list[i])
            c.append(category1_tuple)
        category1_field.choices = c



        #filtered_sub = subjectInfo.objects.filter(user_id=sn)
        detail_params = {
            'form':form,
            #'filtered_sub':filtered_sub
        }

        time.sleep(2)


        return render(request, 'gv/detail.html', detail_params)


###################################################################################
                               #メインのグラフを出力する画面
#####################################################################################

def mainhome(request):
    value = [request.POST['stunum'], request.POST['password']]


    if request.method == 'POST':
        #formから学籍番号とパスワードの取得
        #入力が正しいか
        try:
            global result
            global list_pie
            global list_bar
            global personal_dataset
            result, list_pie, list_bar, table, personal_dataset = condact(value)
        #正しくなかったら戻る
        except Exception as e:
            print(str(e.args))
            form = userInfoForm()
            index_params = {
            'form':form,
            'message':'正しく入力しなおしてください'
            }
            return render(request, 'gv/index.html', index_params)

        #正しくデータを整形することができるかどうか。

        try:
            #pythonからjsへの値の受け渡し
            global mainhome_params
            mainhome_params = pytojsMaterials(result, list_pie, list_bar, table)
            print(mainhome_params)

        except Exception as e:
            form = userInfoForm()
            index_params = {
            'form':form,
            'message':'正しくデータを得ることができませんでした'
            }
            return render(request, 'gv/index.html', index_params)


        #データベースに登録するかどうか
        stuobj = studentInfo.objects.all()
        t = list(personal_dataset.iloc[0])
        if t[0] not in str(stuobj):
            #user情報の保存
            stuinfo = studentInfo(user_id=t[0], student_grade=t[1],
            enteryear=t[2], seasons=t[3], gpa=t[4])
            stuinfo.save()


            #教科情報の保存
            for i in range(len(table)):
                s = list(table.iloc[i])
                subjectInfomation = subjectInfo(subjectnum=s[0],managementnum=s[1],
                user_id=s[2],subjectname=s[3],unit_int=s[4],grade=s[5],
                grade_score_int=s[6],result_score_int=s[7],year_int=s[8],
                season=s[9],teacher=s[10],gpa_int=s[11],
                category1=s[12],category2=s[13],last_login=s[14],stu_id=stuinfo)
                subjectInfomation.save()



        #ログインしたことの証拠,mainhome_after_loginで使用
        global login
        login = 'ok'
        print(login)
        return render(request, 'gv/mainhome.html', mainhome_params)

    #getでmainhomeにアクセスしてしまった時の処理
    else:
        form = userInfoForm()
        index_params = {
        'form':form,
        'message':'学籍番号とパスワードを入力しよう!'
        }
        return render(request, 'gv/index.html', index_params)
