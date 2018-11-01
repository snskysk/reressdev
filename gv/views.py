import sys
import traceback
import time

#
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
#from .forms import userInfoForm, findForm, find_my_sub_Form, food_pool_Form, find_shop
from .forms import userInfoForm, findForm, find_my_sub_Form, food_pool_Form, find_shop, find_course, find_teacher
from .models import studentInfo, subjectInfo, food_pool
from pycord.main import condact
from pycord.pytojs import pytojsMaterials
from django.db.models import Q, Sum
from django.forms import Select
import threading
import uuid
from collections import Counter
from collections import OrderedDict #順番付き辞書
from django.core.paginator import Paginator


import numpy as np

# Create your views here.

###################################################################################
                                    #2重サブミット防止
#################################################################################
def set_submit_token(request):
    submit_token = str(uuid.uuid4())
    request.session['submit_token'] = submit_token
    return submit_token

def exists_submit_token(request):
    token_in_request = request.POST['submit_token']
    token_in_session = request.session['submit_token']
    if token_in_request == token_in_session:
        status = True
    else:
        status = False
    submit_token = set_submit_token(request)
    return status



######################################################################################
                                     #履修を考えるcourse
###################################################################################
def course(request, num=1):
    try:#sessionが切れていないか確認
        sn = request.session['stunum']  #学籍番号をsessionから持ってくる
    except:
        form = userInfoForm()
        index_params = {
            'form':form,
            'message':'学籍番号とパスワードを入力しよう'

            }
        return render(request, 'gv/hp.html', index_params)
    enter_year = sn[:2]   #学籍番号から入学年度の取得
    facu_depa = sn[2:4]  #学籍番号から学部学科の取得
    stu_obj = studentInfo.objects.filter(user_id__contains=facu_depa) #データベースから同じ学部学科の人を取得
    sub_obj = subjectInfo.objects.filter(user_id__contains=facu_depa) #データベースから同じ学部学科の授業を取得
    sub_obj = sub_obj.exclude(category1__contains='必') #必修を除く

    if request.method == 'POST':
        form = find_course(request.POST)
        make_list('category1','category1',sn,form)
        now_field = form.fields['category1'].choices
        #選択肢から必修を取り除く
        new_field = [e for e in now_field if '必' not in e[1]]
        form.fields['category1'].choices = new_field
        category1 = request.POST['category1']
        if len(category1) is not 0:
            sub_obj = sub_obj.filter(category1=category1)
        sub_list = sub_obj.values_list('subjectname', flat=True)#授業名でリストを取得(重複あり)
        sub_list_counter = Counter(sub_list).most_common() #授業の数(多い順)

        page=Paginator(sub_list_counter,10)

        course_params = {
            'form':form,
            'sub_list_counter':page.get_page(num),
        }
        return render(request, 'gv/course.html', course_params)


    sub_list = sub_obj.values_list('subjectname', flat=True)#授業名でリストを取得(重複あり)
    sub_list_counter = Counter(sub_list).most_common() #授業の数(多い順)


    ###############paginator######################
    page = Paginator(sub_list_counter,10)
    ##############################################

    form = find_course()
    make_list('category1','category1',sn,form)
    now_field = form.fields['category1'].choices
    #選択肢から必修を取り除く
    new_field = [e for e in now_field if '必' not in e[1]]
    form.fields['category1'].choices = new_field
    course_params = {
        'sub_obj':sub_obj,
        'form':form,
        #'sub_list_counter':sub_list_counter,
        'sub_list_counter':page.get_page(num),
        }
    return render(request, 'gv/course.html', course_params)

def sirabasu(request):
    sub_name=request.POST['sub-name']#授業名を取得
    subinfo = subjectInfo.objects.filter(subjectname=sub_name)[0]#データベースから該当する授業を取得
    sub_num = subinfo.subjectnum#教科番号を取得
    #now_url = get_sirabasu(sub_name, sub_num)

    url = 'https://sy.rikkyo.ac.jp/timetable/slbsskgr.do'
    url = url + '?'
    #科目名を追加
    url = url + 'value(kouginm)={}&'.format(sub_name)
    url = url + 'value(kamnumText1)={}&'.format(sub_num[:3])
    url = url + 'value(kamnumText2)={}&'.format(sub_num[3])
    url = url + 'value(kamnumText3)={}&'.format(sub_num[4])
    url = url + 'value(kamnumText4)={}&'.format(sub_num[5])
    url = url + 'value(kamnumText5)={}'.format(sub_num[6])
    print(url)


    sirabasu_params={}
    return HttpResponseRedirect('{}'.format(url))
    #return render(request, 'gv/teacher_search.html', sirabasu_params)

def teacher_search(request):
    sub_obj = subjectInfo.objects.all()
    teacher_list_space = list(set(list(subjectInfo.objects.values_list('teacher', flat=True))))#すべての先生のリスト(重複なし)
    teacher_list = [i.replace('　', '') for i in teacher_list_space]#先生の名前スペースなし
    #各先生の授業のリストを生成(ex:{'A先生':[B,C,D]})
    teacher_sub_dict = {teacher_name.replace('　', ''):list(set(subjectInfo.objects.filter(teacher__contains=teacher_name).values_list('subjectname', flat=True))) for teacher_name in teacher_list_space}


    if request.method == 'POST':
        form = find_teacher(request.POST)
        t_name = request.POST['t_name']
        t_sub = request.POST['t_sub']
        #もしスペースありで入力されたら訂正
        if '　' in t_name:
            t_name = t_name.replace('　','')
        try:
            index_teacher_list = teacher_list.index(t_name)#index番号を取得
            t_name=teacher_list_space[index_teacher_list]#実際にデータベースで検索するスペースありの先生の名前
        except:
            form = find_teacher()
            nums = [0,0,0,0]
            grade_list_sample = ['S','A','B','C']

            teacher_search_params = {
                'form':form,
                'nums':nums,
                'grade_list_sample':grade_list_sample,
                'teacher_list':teacher_list,
                'teacher_sub_dict':teacher_sub_dict,
                'r_form':'成績判定統計',
            }
            return render(request, 'gv/teacher_search.html', teacher_search_params)
        sub_obj = sub_obj.filter(teacher=t_name)
        #授業のフィルター
        if len(t_sub) is not 0:
            sub_obj = sub_obj.filter(subjectname=t_sub)

        num_sub = len(sub_obj)#その先生の授業数
        grade_list_dict = OrderedDict({'Ｓ':0,'Ａ':0,'Ｂ':0,'Ｃ':0}) #順番がたぶん大事
        grade_list = sub_obj.values_list('grade', flat=True)#成績判定を取得(重複あり)
        grade_list_dict_new = Counter(grade_list) #授業の数
        grade_list_dict.update(grade_list_dict_new) #辞書をupdate
        nums = grade_list_dict.values()
        nums = list(nums)#リストにする
        try:#入力ミスのとき0で割られるのを防ぐ
            #p = [(num / mum) * 100 for num,mum in zip(nums,[num_sub]*len(nums))]#確立を計算
            grade_list_sample = list(grade_list_dict.keys())
            #計算結果を丸める
            #p = list(map(round, p, [0]*len(p)))

            teacher_search_params = {
                'message':'ok,',
                'form':form,
                'sub_obj':sub_obj,
                'nums':nums,
                'grade_list_sample':grade_list_sample,
                'teacher_list':teacher_list,
                'teacher_sub_dict':teacher_sub_dict,
                'r_form':'{}  {}'.format(t_name,t_sub).replace('　','')
            }
            return render(request, 'gv/teacher_search.html', teacher_search_params)
        except:
            form = find_teacher()
            nums = [0,0,0,0]
            grade_list_sample = ['S','A','B','C']

            teacher_search_params = {
                'form':form,
                'nums':nums,
                'grade_list_sample':grade_list_sample,
                'teacher_list':teacher_list,
                'teacher_sub_dict':teacher_sub_dict,
                'r_form':'成績判定統計',
            }
            return render(request, 'gv/teacher_search.html', teacher_search_params)

    form = find_teacher()
    nums = [0,0,0,0]
    grade_list_sample = ['S','A','B','C']

    teacher_search_params = {
        'message':'',
        'form':form,
        'nums':nums,
        'grade_list_sample':grade_list_sample,
        'teacher_list':teacher_list,
        'teacher_sub_dict':teacher_sub_dict,
        'r_form':'成績判定統計',
    }
    return render(request, 'gv/teacher_search.html', teacher_search_params)

def inquiry(request):
    inquiry_params = {}
    return render(request, 'gv/inquiry.html', inquiry_params)

###################################################################################
                                    #トップページ
######################################################################################
"""
def hp(request):
    request.session.flush()
    form = userInfoForm()
    index_params = {
        'form':form,
        'message':'学籍番号とパスワードを入力してください',
        }

    return render(request, 'gv/hp.html', index_params)
"""

def hp(request):
    form = userInfoForm()
    index_params = {
        'form':form,
        'message':'',
        }

    return render(request, 'gv/hp.html', index_params)

def flush(request):
    request.session.flush()
    form = userInfoForm()
    index_params = {
        'form':form,
        'message':'',
        }

    return render(request, 'gv/hp.html', index_params)
###################################################################################
                                    #停止
##################################################################################
def info(request):
    return render(request, 'gv/informations.html')

def index(request):
    form = userInfoForm()
    index_params = {
        'form':form,
        'message':'学籍番号とパスワードを入力してください',
        }

    return render(request, 'gv/hp.html', index_params)

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
            return render(request, 'gv/hp.html', params)


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
            return render(request, 'gv/hp.html', params)

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
        return render(request, 'gv/hp.html', params)

###################################################################################
                               #メインのグラフを出力する画面
#####################################################################################
#from django.utils.functional import cached_property
#@cached_property
def mainhome(request):

    if request.method == 'POST':
        value = [request.POST['stunum'], request.POST['password']]

        ##mainhomeすらログインしたことがあるuserなら戻す##
        ##################################################
        #学籍番号を大文字に変換
        if not value[0].islower():
            short_cut_sn = value[0].lower()
        else:
            short_cut_sn = value[0]
        stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
        if short_cut_sn in stuobj:#もしすでに登録されているなら

            try:#もしsessionが残っているなら
                mainhome_after_login_params = {}
                str_name = request.session['str_name']
                mainhome_after_login_params['str_name'] = str_name
                gpa = request.session['gpa']
                mainhome_after_login_params['gpa'] = gpa
                #gradeAchievement = request.session['gradeAchievement']
                #mainhome_after_login_params['gradeAchievement'] = gradeAchievement
                kind_name = request.session['kind_name']
                kind_name = kind_name[1:-1].replace(' ','').replace("'",'').split(',')
                mainhome_after_login_params['kind_name'] = kind_name
                Achivement_list = request.session['Achivement_list']
                Achivement_list = Achivement_list[1:-1].replace(' ','').replace("'",'').split(',')
                mainhome_after_login_params['Achivement_list'] = Achivement_list
                unitOfcircle = request.session['unitOfcircle']
                unitOfcircle = unitOfcircle[1:-1].replace(' ','').replace("'",'').split(',')
                for i,j in enumerate(unitOfcircle):
                    num = int(unitOfcircle[i])
                    unitOfcircle[i] = num
                mainhome_after_login_params['unitOfcircle'] = unitOfcircle
                gradeOfcircle = request.session['gradeOfcircle']
                gradeOfcircle = gradeOfcircle[1:-1].replace(' ','').replace("'",'').split(',')
                mainhome_after_login_params['gradeOfcircle'] = gradeOfcircle
                #residual_unit = request.session['residual_unit']
                #residual_unit = residual_unit[1:-1].replace(' ','').replace("'",'').split(',')
                #mainhome_after_login_params['residual_unit'] = residual_unit
                #on_course = request.session['on_course']
                #on_course = on_course[1:-1].replace(' ','').replace("'",'').split(',')
                #ainhome_after_login_params['on_course'] = on_course

                residual_num = request.session['residual_num']
                mainhome_after_login_params['residual_num'] = residual_num
                get_num = request.session['get_num']
                mainhome_after_login_params['get_num'] = get_num
                on_num = request.session['on_num']
                mainhome_after_login_params['on_num'] = on_num
                #棒グラフのsession
                kind_name_bou = request.session['kind_name_bou']
                mainhome_after_login_params['kind_name_bou'] = kind_name_bou
                residual_unit_bou = request.session['residual_unit_bou']
                mainhome_after_login_params['residual_unit_bou'] = residual_unit_bou
                on_course_bou = request.session['on_course_bou']
                mainhome_after_login_params['on_course_bou'] = on_course_bou
                return render(request, 'gv/mainhome.html', mainhome_after_login_params)

            except:
                pass
        else:
            pass








        #formから学籍番号とパスワードの取得
        #入力が正しいか
        try:
            result, list_pie, list_bar, table, personal_dataset, kyoushoku_c = condact(value)
        #正しくなかったら戻る
        except Exception as e:
            pprint.pprint(str(e.args))
            form = userInfoForm()
            index_params = {
            'form':form,
            'message':'正しく入力しなおしてください'
            }
            return render(request, 'gv/hp.html', index_params)

        #正しくデータを整形することができるかどうか。

        try:
            #pythonからjsへの値の受け渡し
            mainhome_params = pytojsMaterials(result, list_pie, list_bar, table, kyoushoku_c)
            for k in mainhome_params.keys():
                request.session['{}'.format(k)] = str(mainhome_params[k])
        except Exception as e:
            print(str(e.args))
            form = userInfoForm()
            index_params = {
            'form':form,
            'message':'正しくデータを得ることができませんでした'
            }
            return render(request, 'gv/hp.html', index_params)


        #データベースに登録するかどうか
        stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
        t = list(personal_dataset.iloc[0])

        #学籍番号を大文字に変換
        if not t[0].islower():
            lowerd_sn = t[0].lower()
        else:
            lowerd_sn = t[0]

        request.session['stunum'] = lowerd_sn #settionに学籍番号を登録


        if lowerd_sn not in stuobj:
            print('保存-------------------------------------------------------------------')
            #user情報の保存
            stuinfo = studentInfo(user_id=lowerd_sn, student_grade=t[1],
            enteryear=t[2], seasons=t[3], gpa=t[4])
            stuinfo.save()


            #教科情報の保存
            for i in range(len(table)):
                s = list(table.iloc[i])
                subjectInfomation = subjectInfo(subjectnum=s[0],managementnum=s[1],
                user_id=lowerd_sn,subjectname=s[3],unit_int=s[4],grade=s[5],
                grade_score_int=s[6],result_score_int=s[7],year_int=s[8],
                season=s[9],teacher=s[10],gpa_int=s[11],
                category1=s[12],category2=s[13],last_login=s[14],stu_id=stuinfo)
                subjectInfomation.save()


        #ログインしたことの証拠,mainhome_after_loginで使用
        return render(request, 'gv/mainhome.html', mainhome_params)

    #getでmainhomeにアクセスしてしまった時の処理
    else:
        form = userInfoForm()
        index_params = {
        'form':form,
        'message':'学籍番号とパスワードを入力しよう!'
        }
        return render(request, 'gv/hp.html', index_params)

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
        #gradeAchievement = request.session['gradeAchievement']
        #mainhome_after_login_params['gradeAchievement'] = gradeAchievement
        kind_name = request.session['kind_name']
        kind_name = kind_name[1:-1].replace(' ','').replace("'",'').split(',')
        mainhome_after_login_params['kind_name'] = kind_name
        Achivement_list = request.session['Achivement_list']
        Achivement_list = Achivement_list[1:-1].replace(' ','').replace("'",'').split(',')
        mainhome_after_login_params['Achivement_list'] = Achivement_list
        unitOfcircle = request.session['unitOfcircle']
        unitOfcircle = unitOfcircle[1:-1].replace(' ','').replace("'",'').split(',')
        for i,j in enumerate(unitOfcircle):
            num = int(unitOfcircle[i])
            unitOfcircle[i] = num
        mainhome_after_login_params['unitOfcircle'] = unitOfcircle
        gradeOfcircle = request.session['gradeOfcircle']
        gradeOfcircle = gradeOfcircle[1:-1].replace(' ','').replace("'",'').split(',')
        mainhome_after_login_params['gradeOfcircle'] = gradeOfcircle
        #residual_unit = request.session['residual_unit']
        #residual_unit = residual_unit[1:-1].replace(' ','').replace("'",'').split(',')
        #mainhome_after_login_params['residual_unit'] = residual_unit
        #on_course = request.session['on_course']
        #on_course = on_course[1:-1].replace(' ','').replace("'",'').split(',')
        #mainhome_after_login_params['on_course'] = on_course

        residual_num = request.session['residual_num']
        mainhome_after_login_params['residual_num'] = residual_num
        get_num = request.session['get_num']
        mainhome_after_login_params['get_num'] = get_num
        on_num = request.session['on_num']
        mainhome_after_login_params['on_num'] = on_num

        #棒グラフのsession
        kind_name_bou = request.session['kind_name_bou']
        mainhome_after_login_params['kind_name_bou'] = kind_name_bou
        residual_unit_bou = request.session['residual_unit_bou']
        mainhome_after_login_params['residual_unit_bou'] = residual_unit_bou
        on_course_bou = request.session['on_course_bou']
        mainhome_after_login_params['on_course_bou'] = on_course_bou

        return render(request, 'gv/mainhome.html', mainhome_after_login_params)

    except Exception:
        mainhome_after_login = 'no'
    #一度mainhomeに入っていれば実行
    #if mainhome_after_login == 'ok':
        #return render(request, 'gv/mainhome.html', mainhome_params)
    #else:
    form = userInfoForm()
    index_params = {
        'form':form,
        'message':'学籍番号とパスワードを入力しよう'
    }
    return render(request, 'gv/hp.html', index_params)



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
        sn = request.session['stunum']

    #ログインしてからでなければ入れない
    except Exception:
        form = userInfoForm()
        index_params = {
            'form':form,
            'message':'学籍番号とパスワードを入力しよう'
        }
        return render(request, 'gv/hp.html', index_params)

    #同じ学年、学科gpaの順位を計算
    same_stu_gpa = sorted(list(studentInfo.objects.filter(user_id__contains=sn[:4]).values_list('gpa', flat=True)),reverse=True)#同じ学年学科のgpaのリスト
    #same_stu_gpa = np.array(sorted(list(studentInfo.objects.filter(user_id__contains=sn[:3]).values_list('gpa', flat=True)),reverse=True))#同じ学年学科のgpaのリスト
    p_num = len(same_stu_gpa)#同じ学年学科の人数
    my_gpa = studentInfo.objects.get(user_id=sn).gpa#自分のgpa
    my_index = [i for i, x in enumerate(same_stu_gpa) if x == my_gpa][0]
    gpa_rank_p = (my_index / p_num) * 100#gpaのランキング(%)
    gpa_rank_width = 50 + (gpa_rank_p/100)*50
    #gpa_rank = same_stu_gpa.index(my_gpa) + 1#自分の順位
    gpa_rank_i = my_index + 1#gpaのランキング(順位)


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

        filtered_sub_gpa = filtered_sub.exclude(grade = '履')
        result_score_int_sum = filtered_sub_gpa.aggregate(Sum('result_score_int'))['result_score_int__sum']
        unit_int_sum = filtered_sub_gpa.aggregate(Sum('unit_int'))['unit_int__sum']


        detail_params = {
            #'gpa_message':'該当科目のgpaは<b><u>'+str(round(gpa,2))+'</u></b><br>    ※Dがある場合正しく計算されません',
            'filtered_sub':filtered_sub,
            'form':form,
            'gpa_rank_p':gpa_rank_p,
            'gpa_rank_i':gpa_rank_i,
            'gpa_rank_width':gpa_rank_width,
            'my_gpa':my_gpa,
            'p_num':p_num,
        }
        return render(request, 'gv/detail.html', detail_params)


    form = find_my_sub_Form()
    filtered_sub = subjectInfo.objects.filter(user_id=sn)#userのみの授業の情報
    filtered_sub_gpa = filtered_sub.exclude(grade = '履')

    make_list('year_int','year',sn,form)#formのリストの中身を変更
    make_list('category1','category1',sn,form)#formのリストの中身を変更


    detail_params = {
        'form':form,
        'filtered_sub':filtered_sub,
        'gpa_rank_p':gpa_rank_p,
        'gpa_rank_i':gpa_rank_i,
        'gpa_rank_width':gpa_rank_width,
        'my_gpa':my_gpa,
        'p_num':p_num,
        #'gpa_message':'gpaは<b><u>'+str(round(gpa,2))+'</u></b><br>    ※Dがある場合正しく計算されません'
    }
    return render(request, 'gv/detail.html', detail_params)

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
