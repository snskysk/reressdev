import sys
import traceback
import time

#
from django.shortcuts import render, redirect
from .forms import userInfoForm, findForm, find_my_sub_Form, food_pool_Form, find_shop
from .models import studentInfo, subjectInfo, food_pool
from pycord.main import condact
from pycord.pytojs import pytojsMaterials
from django.db.models import Q, Sum
from django.forms import Select
import threading


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

def info(request):
    return render(request, 'gv/informations.html')
###################################################################################
                                    #ログイン画面
##################################################################################
def index(request):
    form = userInfoForm()
    index_params = {
        'form':form,
        'message':'学籍番号とパスワードを入力してください',
        }

    return render(request, 'gv/index.html', index_params)

####################################################################################
                                #ログイン後のメイン画面用
####################################################################################
def mainhome_after_login(request):
    try: #ログインしているか確かめる
        #mainhome_after_login = login
        #print(mainhome_after_login)
        mainhome_after_login_params = {}
        str_name = request.session['str_name']
        mainhome_after_login_params['str_name'] = str_name
        gpa = request.session['gpa']
        mainhome_after_login_params['gpa'] = gpa
        gradeAchievement = request.session['gradeAchievement']
        mainhome_after_login_params['gradeAchievement'] = gradeAchievement
        kind_name = request.session['kind_name']
        kind_name = kind_name[1:-1].replace(' ','').replace("'",'').split(',')
        mainhome_after_login_params['kind_name'] = kind_name
        Achivement_list = request.session['Achivement_list']
        Achivement_list = Achivement_list[1:-1].replace(' ','').replace("'",'').split(',')
        mainhome_after_login_params['Achivement_list'] = Achivement_list
        unitOfcircle = request.session['unitOfcircle']
        unitOfcircle = unitOfcircle[1:-1].replace(' ','').replace("'",'').split(',')
        mainhome_after_login_params['unitOfcircle'] = unitOfcircle
        gradeOfcircle = request.session['gradeOfcircle']
        gradeOfcircle = gradeOfcircle[1:-1].replace(' ','').replace("'",'').split(',')
        mainhome_after_login_params['gradeOfcircle'] = gradeOfcircle
        residual_unit = request.session['residual_unit']
        residual_unit = residual_unit[1:-1].replace(' ','').replace("'",'').split(',')
        mainhome_after_login_params['residual_unit'] = residual_unit
        on_course = request.session['on_course']
        on_course = on_course[1:-1].replace(' ','').replace("'",'').split(',')
        mainhome_after_login_params['on_course'] = on_course


        return render(request, 'gv/mainhome.html', mainhome_after_login_params)


    except Exception:
        mainhome_after_login = 'no'
    #一度mainhomeに入っていれば実行
    if mainhome_after_login == 'ok':


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


######################################################################################
                                     #詳細画面
###################################################################################

######################################################################################################
                            #フォームを人それぞれで分ける 関数化
######################################################################################################
def make_list(model_name,form_name,sn,form):
    kind_list = list(set(list(subjectInfo.objects.filter(user_id=sn).values_list('{}'.format(model_name), flat=True))))
    the_field = form.fields['{}'.format(form_name)]
    form_list = [('','{}'.format(form_name))]
    for i in range(0, len(kind_list)):
        form_tuple = (kind_list[i],kind_list[i])
        form_list.append(form_tuple)
        the_field.choices = form_list
    return


######################################################################################
                                     #詳細画面
###################################################################################

def detail(request):
    try:
        sn=request.session['stunum']
        #sn = personal_dataset.loc[0,'user_id']   #ログイン中のユーザーの学籍番号
        #sn = '16cb087l'
    #ログインしてからでなければ入れない
    except Exception as e:
        form = userInfoForm()
        index_params = {
            'form':form
        }
        return render(request, 'gv/index.html', index_params)


    if request.method == 'POST':
        form = find_my_sub_Form(request.POST)
        make_list('year_int','year',sn,form)
        make_list('category1','category1',sn,form)
        filtered_sub = subjectInfo.objects.filter(user_id=sn)
        season = request.POST['season']
        grade = request.POST['grade']
        year = request.POST['year']
        category1 = request.POST['category1']
        subname_teacher = request.POST['subname_teacher']

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

        result_score_int_sum = filtered_sub.aggregate(Sum('result_score_int'))['result_score_int__sum']
        unit_int_sum = filtered_sub.aggregate(Sum('unit_int'))['unit_int__sum']
        gpa = result_score_int_sum / unit_int_sum

        detail_params = {
            'gpa_message':'該当科目のgpaは<b><u>'+str(round(gpa,2))+'</u></b><br>    ※Dがある場合正しく計算されません',
            'filtered_sub':filtered_sub,
            'form':form,
        }
        return render(request, 'gv/detail.html', detail_params)
    form = find_my_sub_Form()
    filtered_sub = subjectInfo.objects.filter(user_id=sn)
    result_score_int_sum = filtered_sub.aggregate(Sum('result_score_int'))['result_score_int__sum']
    unit_int_sum = filtered_sub.aggregate(Sum('unit_int'))['unit_int__sum']
    gpa = result_score_int_sum / unit_int_sum
    make_list('year_int','year',sn,form)
    make_list('category1','category1',sn,form)
    detail_params = {
        'form':form,
        'filtered_sub':filtered_sub
    }
    return render(request, 'gv/detail.html', detail_params)



###################################################################################
                               #メインのグラフを出力する画面
#####################################################################################
#from django.utils.functional import cached_property
#@cached_property

def mainhome(request):

    if request.method == 'POST':
        value = [request.POST['stunum'], request.POST['password']]

        request.session['stunum']=value[0]

        #formから学籍番号とパスワードの取得
        #入力が正しいか
        try:
            #global result
            #global list_pie
            #global list_bar
            #global personal_dataset
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
            #global mainhome_params
            mainhome_params = pytojsMaterials(result, list_pie, list_bar, table)

            for k in mainhome_params.keys():
                request.session['{}'.format(k)] = str(mainhome_params[k])


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
        #global login
        login = 'ok'
        return render(request, 'gv/mainhome.html', mainhome_params)

    #getでmainhomeにアクセスしてしまった時の処理
    else:
        form = userInfoForm()
        index_params = {
        'form':form,
        'message':'学籍番号とパスワードを入力しよう!'
        }
        return render(request, 'gv/index.html', index_params)

######################################################################################
                                     #飲食店レビュー
###################################################################################

def review(request):
    form = food_pool_Form()
    review_params = {
        'form':form
    }
    if request.method == 'POST':
        form = food_pool_Form(request.POST)
        form.save()
    return render(request, 'gv/review.html', review_params)

######################################################################################
                                     #飲食店検索
###################################################################################

def shop_search(request):
    if request.method == 'POST':
        form = find_shop(request.POST)
        shop_obj = food_pool.objects.all()
        print(shop_obj)
        shop_name = request.POST['shop_name']
        price = request.POST['price']
        #shop_nameのフィルター
        if len(shop_name) is not 0:
            shop_obj = shop_obj.filter(shop_name__contains=shop_name)
        #価格のフィルター
        if len(price) is not 0:
            shop_obj = shop_obj.filter(price=price)
        shop_search_params = {
            'form':form,
            'shop_obj':shop_obj
        }
        return render(request, 'gv/shop_search.html', shop_search_params)
    shop_obj = food_pool.objects.all()
    form = find_shop()
    shop_search_params = {
        'form':form,
        'shop_obj':shop_obj
    }
    return render(request, 'gv/shop_search.html', shop_search_params)
