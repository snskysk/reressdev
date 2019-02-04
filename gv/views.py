import sys
import traceback
import time

#
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
#from .forms import userInfoForm, findForm, find_my_sub_Form, food_pool_Form, find_shop
from .forms import userInfoForm, findForm, find_my_sub_Form, food_pool_Form, find_shop, find_course, find_teacher, find_sub
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
import pandas as pd
from operator import itemgetter
####### 高速化実験 #######
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
##############
#
from .forms import ggs_counter_Form
#
# Create your views here.

#####################################   view 目次     ######################################
                #トップページ関連
                                    # hp   # substitution　　# flush
                #mainhome関連
                                    # new_data_register    # mainhome　　
                #五大機能関連
                                    # mainhome_after_login
                                    # detail
                                    # course_more
                                    # course
                                    # sub_search
                                    # sirabasu
                                    # more
                                    # teacher_serach
                                    # make_list
                #その他
                                    #pastdata
                                    # counter
                                    # inquiry
                                    # 二重サブミット防止

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                                                                #トップページ関連
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def base(request):
    form = userInfoForm()
    stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
    numbers=len(stuobj)
    request.session['numbers'] = numbers
    try:#sessionが切れていないか確認
        sn = request.session['stunum']  #学籍番号をsessionから持ってくる
        site_map_params = {
            'numbers':numbers,
        }
        return render(request, 'gv/site_map.html',site_map_params)
    except:
        value_0 = 'first_to_fast'
        value = [value_0,1]
        try:#substitutionを利用した高速化処理ーー万が一失敗しても悪影響はない
            result, list_pie, list_bar, table, personal_dataset, kyoushoku_c, passcheck = condact(value)
        except:
            pass
        #mainhome_params = pytojsMaterials(result, list_pie, list_bar, table, kyoushoku_c)
        form = userInfoForm()
        print("---speed_optimisation1の実行が確認されました---")
        hp_params = {
            'form':form,
            #'message':'学籍番号とパスワードを入力しよう',
            'numbers':numbers,

            }
        return render(request, 'gv/hp.html', hp_params)
    index_params = {
        'form':form,
        'message':'',
        'numbers':numbers,
        }

    return render(request, 'gv/hp.html', index_params)

def hp(request):
    form = userInfoForm()
    stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
    numbers=len(stuobj)
    request.session['numbers'] = numbers
    try:#sessionが切れていないか確認
        sn = request.session['stunum']  #学籍番号をsessionから持ってくる
        site_map_params = {
            'numbers':numbers,
        }
        return render(request, 'gv/site_map.html',site_map_params)
    except:
        value_0 = 'first_to_fast'
        value = [value_0,1]
        try:#substitutionを利用した高速化処理ーー万が一失敗しても悪影響はない
            result, list_pie, list_bar, table, personal_dataset, kyoushoku_c, passcheck = condact(value)
        except:
            pass
        #mainhome_params = pytojsMaterials(result, list_pie, list_bar, table, kyoushoku_c)
        form = userInfoForm()
        print("---speed_optimisation1の実行が確認されました---")
        hp_params = {
            'form':form,
            #'message':'学籍番号とパスワードを入力しよう',
            'numbers':numbers,

            }
        return render(request, 'gv/hp.html', hp_params)
    index_params = {
        'form':form,
        'message':'',
        'numbers':numbers,
        }

    return render(request, 'gv/hp.html', index_params)

def substitution(request):#スクレイピング高速化用
    return render(request, 'gv/demo_gd.html')

def flush(request):#flush関数自体はsessionのflushを行わない。hp.htmlを返すためのもの。flushはmainhome関数内で行う。
    #request.session.flush()
    form = userInfoForm()
    stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
    numbers=len(stuobj)

    #URL="https://rs.rikkyo.ac.jp/"
    #try:
    #    driver = webdriver.PhantomJS()
    #except:#ローカルはphantomJSが使えないのでchromeに
    #    driver = webdriver.Chrome()
    #driver.get(URL)
    #driver.close()
    index_params = {
        'form':form,
        'message':'',
        'numbers':numbers,
        }

    return render(request, 'gv/hp.html', index_params)



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                                                                #mainhome関連
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

##########################################################################
                            #状況に応じてデータベースへ保存または削除＆上書き
##########################################################################
def new_data_register(st_data,sub_data,judgement_number,personal_number):
    #user情報の保存
    if judgement_number == 1:
        stuinfo = studentInfo(user_id=personal_number, student_grade=st_data[1],
        enteryear=st_data[2], seasons=st_data[3], gpa=st_data[4])
        stuinfo.save()
    elif judgement_number == 2:
        studentInfo.objects.filter(user_id__contains=personal_number).delete() #生徒情報を一度削除
        stuinfo = studentInfo(user_id=personal_number, student_grade=st_data[1],
        enteryear=st_data[2], seasons=st_data[3], gpa=st_data[4])
        stuinfo.save()
    else:
        pass
    #教科情報の保存
    for i in range(len(sub_data)):
        s = list(sub_data.iloc[i])
        subjectInfomation = subjectInfo(subjectnum=s[0],managementnum=s[1],
        user_id=personal_number,subjectname=s[3],unit_int=s[4],grade=s[5],
        grade_score_int=s[6],result_score_int=s[7],year_int=s[8],
        season=s[9],teacher=s[10],gpa_int=s[11],
        category1=s[12],category2=s[13],last_login=s[14],stu_id=stuinfo)
        subjectInfomation.save()


def mainhome(request):
    stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
    numbers=len(stuobj)
    start = time.time()
    if request.method == 'POST':
        value = [request.POST['stunum'], request.POST['password']]

        ##mainhomeすらログインしたことがあるuserなら戻す##
        ##################################################
        #学籍番号を大文字に変換
        if not value[0].islower():
            short_cut_sn = value[0].lower()
        else:
            short_cut_sn = value[0]

        #stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
        #numbers=len(stuobj)
        if value[0]=='systemcall' and value[1]=='counter':
            counter_params={
                'numbers':numbers,
            }
            return render(request,'gv/counter.html',counter_params)
        else:
            pass
        if value[0]=='flush':
            request.session.flush()
            form = userInfoForm()
            index_params = {
            'numbers':numbers,
            'form':form,
            #'message':''
            }
            return render(request, 'gv/hp.html', index_params)
        else:
            pass
        request.session.flush()
        if short_cut_sn in stuobj:#もしすでに登録されているなら

            try:#もしsessionが残っているなら #ここはもう要らないかも
                mainhome_after_login_params = {}
                ##str_name = request.session['str_name']
                ##mainhome_after_login_params['str_name'] = str_name
                ##gpa = request.session['gpa']
                ##mainhome_after_login_params['gpa'] = gpa
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
                return render(request, 'gv/site_map.html', mainhome_after_login_params)

            except:
                pass
        else:
            pass

        middle_time = np.round(time.time() - start,1)
        print('---condactまでの経過時間 {0}秒---'.format(middle_time))

        #formから学籍番号とパスワードの取得
        #入力が正しいか
        try:#以下の複数のifでmain.pyから受け取ったpasscheckによって工程を進めるかエラーとして吐き出すかを決定
            result, list_pie, list_bar, table, personal_dataset, kyoushoku_c, passcheck = condact(value)
            if passcheck==1:
                pass
            elif passcheck==2:
                form = userInfoForm()
                index_params = {
                'numbers':numbers,
                'form':form,
                'message':'お手数ですが再度お試しください。データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ２'
                }
                return render(request, 'gv/hp.html', index_params)

            elif passcheck==3:
                form = userInfoForm()
                index_params = {
                'form':form,
                'numbers':numbers,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ３'
                }
                return render(request, 'gv/hp.html', index_params)

            elif passcheck==4:
                form = userInfoForm()
                index_params = {
                'form':form,
                'numbers':numbers,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ４'
                }
                return render(request, 'gv/hp.html', index_params)

            elif passcheck==5:
                form = userInfoForm()
                index_params = {
                'form':form,
                'numbers':numbers,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ５'
                }
                return render(request, 'gv/hp.html', index_params)

            elif passcheck==11:
                form = userInfoForm()
                index_params = {
                'form':form,
                'numbers':numbers,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ１１'
                }
                return render(request, 'gv/hp.html', index_params)
            elif passcheck==12:
                form = userInfoForm()
                index_params = {
                'form':form,
                'numbers':numbers,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ１２'
                }
                return render(request, 'gv/hp.html', index_params)

            else:
                form = userInfoForm()
                index_params = {
                'form':form,
                'numbers':numbers,
                'message':'学生番号かパスワードが間違っている可能性があります'
                }
                return render(request, 'gv/hp.html', index_params)         #正しくなかったら戻る
        except Exception as e:
            form = userInfoForm()
            index_params = {
            'form':form,
            'numbers':numbers,
            'message':'お手数ですが、再度お試しください。それでもご利用になれない場合は、よろしければ学年と学部学科、特殊な授業の履修履歴などがあれば明記の上お問い合わせください。'
            }
            return render(request, 'gv/hp.html', index_params)

        #正しくデータを整形することができるかどうか。

        try:
            #pythonからjsへの値の受け渡し
            mainhome_params = pytojsMaterials(result, list_pie, list_bar, table, kyoushoku_c)
            mainhome_params['numbers'] = numbers
            for k in mainhome_params.keys():
                request.session['{}'.format(k)] = str(mainhome_params[k])

        except Exception as e:
            print(str(e.args))
            form = userInfoForm()
            index_params = {
            'form':form,
            'numbers':numbers,
            'message':'正しくデータを得ることができませんでした'
            }
            return render(request, 'gv/hp.html', index_params)


        #データベースに登録するかどうか
        #stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
        t = list(personal_dataset.iloc[0])

        #学籍番号を大文字に変換
        if not t[0].islower():
            lowerd_sn = t[0].lower()
        else:
            lowerd_sn = t[0]

        request.session['stunum'] = lowerd_sn #settionに学籍番号を登録


        if lowerd_sn not in stuobj:
            print('---新規ユーザーのデータを保存------------------------------------')
            new_data_register(t,table,1,lowerd_sn)
        else:
            ndc = len(table)#new_data_count
            old_data = subjectInfo.objects.filter(user_id__contains=lowerd_sn)  #old_data変数として以後使うため2フェーズに分けている
            odc = len(old_data)#old_data_count
            nd_taking = len(table[table.iloc[:,5]=="履"])  #new_dataに含まれる「履」の数
            od_taking = len(old_data.filter(grade="履"))   #old_dataに含まれる「履」の数
            try:
                if ndc > odc:
                    old_data.exclude(grade='Ｄ').delete()
                    new_data_register(t,table,2,lowerd_sn)
                    print("---すでに登録されているが新たなデータが古いデータより多いパターン---")
                elif ndc <= odc and nd_taking < od_taking:
                    nd_normal = len(table[table.iloc[:,5]!="履"][table.iloc[:,5]!="Ｑ"][table.iloc[:,5]!="Ｄ"][table.iloc[:,5]!="欠"])
                    od_normal = len(subjectInfo.objects.filter(user_id__contains=lowerd_sn).exclude(grade='履').exclude(grade='Ｑ').exclude(grade='Ｄ').exclude(grade='欠'))
                    if nd_normal == od_normal:
                        old_data.filter(grade="履").delete()
                        old_data.filter(grade="Ｑ").delete()
                        table[table.iloc[:,5]=="履"][table.iloc[:,5]=="Ｑ"]
                        new_data_register(t,table,0,lowerd_sn)
                        print("---すでに登録されているが、「履」が「Ｑ」になった授業があるパターン---")
                    elif nd_normal > od_normal:
                        old_data.exclude(grade='Ｄ').delete()
                        new_data_register(t,table,2,lowerd_sn)
                        print("---すでに登録されており、「履」の成績結果が出て内容が書き換わったパターン---")
                    else:
                        print("---想定外のパターン1---")
                elif ndc < odc and nd_taking == od_taking:
                    print("---すでに登録されており、過去にとったＤが成績表から消えてしまった場合---")
                else:
                    print("---すでに登録されており、データに何の変化もないパターン---")
            except:
                pass
        elapsed_time = np.round(time.time() - start,1)
        print('---mainhome全プロセス経過時間 {0}秒---'.format(elapsed_time))
        #ログインしたことの証拠,mainhome_after_loginで使用
        return render(request, 'gv/site_map.html', mainhome_params)

    #getでmainhomeにアクセスしてしまった時の処理
    else:
        form = userInfoForm()
        #stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
        #numbers=len(stuobj)

        index_params = {
            'form':form,
            'message':'学籍番号とパスワードを入力しよう',
            'numbers':numbers,

        }
        return render(request, 'gv/hp.html', index_params)



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                                                                #五大機能関連
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

##########################################################################
                                #ログイン後のメイン画面用
##########################################################################

def mainhome_after_login(request):
    try: #ログインしているか確かめる
        #mainhome_after_login = login
        #print(mainhome_after_login)
        mainhome_after_login_params = {}
        ##str_name = request.session['str_name']
        ##mainhome_after_login_params['str_name'] = str_name
        ##gpa = request.session['gpa']
        ##mainhome_after_login_params['gpa'] = gpa
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
    stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
    numbers=len(stuobj)

    index_params = {
        'form':form,
        'message':'学籍番号とパスワードを入力しよう',
        'numbers':numbers,

    }
    return render(request, 'gv/hp.html', index_params)


def detail(request):
    stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
    numbers=len(stuobj)
    gg_lists = {
        'aa':'キリスト教学科','ac':'史学科','ae':'教育学科','am':'文学科{英米文学専修}','an':'文学科{ドイツ文学専修}',
        'as':'文学科{フランス文学専修}','at':'文学科{日本文学専修}','au':'文学部{文藝・思想専修}','ba':'経済学科','bc':'会計ファイナンス学科',
        'bd':'経済政策学科','bm':'経営学科','bn':'国際経営学科','ca':'数学科','cb':'物理学科','cc':'化学科','cd':'生命理学科',
        'da':'社会学科','dd':'現代文化学科','de':'メディア社会学科','dm':'異文化コミュニケーション学科','ea':'法学科','ec':'政治学科','ed':'国際ビジネス法学科',
        'ib':'福祉学科','ic':'コミュニティ政策学科','id':'スポーツウエルネス学科','hm':'心理学科','hn':'映像身体学科','ha':'観光学科','hb':'交流文化学科'
    }

    try:
        sn = request.session['stunum']
        belongs = gg_lists[sn[2:4]]

    #ログインしてからでなければ入れない
    except Exception:
        form = userInfoForm()
        index_params = {
            'form':form,
            'message':'学籍番号とパスワードを入力しよう',
            'numbers':numbers,
        }
        return render(request, 'gv/hp.html', index_params)


    #同じ学年
    same_stu_gpa1 = sorted(list(studentInfo.objects.filter(user_id__startswith=sn[:2]).values_list('gpa', flat=True)),reverse=True)#同じ学年学科のgpaのリスト
    p_num1 = len(same_stu_gpa1)#同じ学年学科の人数
    my_gpa1 = studentInfo.objects.get(user_id=sn).gpa#自分のgpa
    my_index1 = [i for i, x in enumerate(same_stu_gpa1) if x == my_gpa1][0]
    gpa_rank_p1 = (my_index1 / p_num1) * 100#gpaのランキング(%)
    gpa_rank_width1 = 50 + (gpa_rank_p1/100)*50
    gpa_rank_i1 = my_index1 + 1#gpaのランキング(順位)
    ran_1 = [p_num1, my_gpa1, gpa_rank_p1, gpa_rank_width1, gpa_rank_i1]#ランキングに必要なデータの配列

    #同じ学年、学科gpaの順位を計算
    same_stu_gpa2 = sorted(list(studentInfo.objects.filter(user_id__startswith=sn[:4]).values_list('gpa', flat=True)),reverse=True)#同じ学年学科のgpaのリスト
    p_num2 = len(same_stu_gpa2)#同じ学年学科の人数
    my_gpa2 = studentInfo.objects.get(user_id=sn).gpa#自分のgpa
    my_index2 = [i for i, x in enumerate(same_stu_gpa2) if x == my_gpa2][0]
    gpa_rank_p2 = (my_index2 / p_num2) * 100#gpaのランキング(%)
    gpa_rank_width2 = 50 + (gpa_rank_p2/100)*50
    gpa_rank_i2 = my_index2 + 1#gpaのランキング(順位)
    ran_2 = [p_num2, my_gpa2, gpa_rank_p2, gpa_rank_width2, gpa_rank_i2]#ランキングに必要なデータの配列


    filtered_sub = subjectInfo.objects.filter(user_id=sn)#userのみの授業の情報
    category1_list = list(filtered_sub.values_list('category1', flat=True).distinct())
    year_list = list(filtered_sub.values_list('year_int', flat=True).distinct())
    detail_params = {
        'filtered_sub':filtered_sub,
        'category1_list':category1_list,
        'year_list':year_list,
        'ran_1':ran_1,
        'ran_2':ran_2,
        'sn':sn,
        'belongs':belongs,##########################################追加する部分3番
    }
    return render(request, 'gv/detail.html', detail_params)



##########################################################################
                #履修を考えるcourseで他学科を見るときに使う関数
##########################################################################
def course_more(request):
    gg_lists = {'aa':'キリスト教学科','ac':'史学科','ae':'教育学科','am':'文学科{英米文学専修}','an':'文学科{ドイツ文学専修}','as':'文学科{フランス文学専修}','at':'文学科{日本文学専修}','au':'文学部{文芸・思想専修}','ba':'経済学科','bc':'会計ファイナンス学科','bd':'経済政策学科','bm':'経営学科','bn':'国際経営学科','ca':'数学科','cb':'物理学科','cc':'化学科','cd':'生命理学科','da':'社会学科','dd':'現代文化学科','de':'メディア社会学科','dm':'異文化コミュニケーション学科','ea':'法学科','ec':'政治学科','ed':'国際ビジネス法学科','ib':'福祉学科','ic':'コミュニティ政策学科','id':'スポーツウエルネス学科','hm':'心理学科','hn':'映像身体学科','ha':'観光学科','hb':'交流文化学科'}
    gakka = request.GET.get('name')
    sub_obj_origin = subjectInfo.objects.filter(user_id__contains=gakka) #データベースから同じ学部学科の授業を取得
    sub_obj = sub_obj_origin.exclude(category1__contains='必').exclude(grade='履') #必修と履修中を除く
    sub_list = sub_obj.values_list('subjectname', flat=True)#授業名でリストを取得(重複あり)
    sub_list_counter = Counter(sub_list).most_common()[:20] #授業の数(多い順)
    sub_list_counter = [(a[0],a[1],np.round(np.average(list(sub_obj.filter(subjectname=a[0]).values_list('grade_score_int',flat=True))),2)) for a in sub_list_counter]
    course_more_params = {
        'sub_list_counter':sub_list_counter,
        'gakka':gakka,
        'gakka_j':gg_lists[gakka],
    }
    return render(request, 'gv/course_more.html', course_more_params)

##########################################################################
                                     #履修を考えるcourse
##########################################################################
def course(request, num=1):
    gg_lists = {'aa':'キリスト教学科','ac':'史学科','ae':'教育学科','am':'文学科{英米文学専修}','an':'文学科{ドイツ文学専修}','as':'文学科{フランス文学専修}','at':'文学科{日本文学専修}','au':'文学部{文芸・思想専修}','ba':'経済学科','bc':'会計ファイナンス学科','bd':'経済政策学科','bm':'経営学科','bn':'国際経営学科','ca':'数学科','cb':'物理学科','cc':'化学科','cd':'生命理学科','da':'社会学科','dd':'現代文化学科','de':'メディア社会学科','dm':'異文化コミュニケーション学科','ea':'法学科','ec':'政治学科','ed':'国際ビジネス法学科','ib':'福祉学科','ic':'コミュニティ政策学科','id':'スポーツウエルネス学科','hm':'心理学科','hn':'映像身体学科','ha':'観光学科','hb':'交流文化学科'}
    stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
    numbers=len(stuobj)
    try:#sessionが切れていないか確認
        sn = request.session['stunum']  #学籍番号をsessionから持ってくる
    except:
        form = userInfoForm()
        hp_params = {
            'form':form,
            'message':'学籍番号とパスワードを入力しよう',
            'numbers':numbers,

            }
        return render(request, 'gv/hp.html', hp_params)
    enter_year = sn[:2]   #学籍番号から入学年度の取得
    facu_depa = sn[2:4]  #学籍番号から学部学科の取得
    stu_obj = studentInfo.objects.filter(user_id__contains=facu_depa) #データベースから同じ学部学科の人を取得
    sub_obj_origin = subjectInfo.objects.filter(user_id__contains=facu_depa) #データベースから同じ学部学科の授業を取得
    sub_obj = sub_obj_origin.exclude(category1__contains='必').exclude(grade='履') #必修を除く
    category1_list_course = list(sub_obj.values_list('category1', flat=True).distinct())#必修以外の授業リスト



    #追加(12月1日)全カリ用
    zenkari_ranking = Counter(subjectInfo.objects.filter(
        Q(category1='＊学びの精神＊')|
        Q(category1='＊多彩な学び，スポ＊')
    ).exclude(grade='履').exclude(grade='Q').values_list('subjectname',flat=True)).most_common()[:20]
    zenkari_ranking = [(a[0],a[1],np.round(np.average(list(subjectInfo.objects.filter(subjectname=a[0]).exclude(grade='履').exclude(grade='Q').values_list('grade_score_int',flat=True))),2)) for a in zenkari_ranking]

    #gpa順にソートした全カリのリスト
    zenkari_ranking_sorted_gpa = sorted(zenkari_ranking, key=lambda zenkari_ranking: zenkari_ranking[2], reverse=True)

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
        sub_list_counter = Counter(sub_list).most_common()[:20] #授業の数(多い順)
        #変更された1行(読みずらいが高速)
        sub_list_counter = [(a[0],a[1],np.round(np.average(list(sub_obj.filter(subjectname=a[0]).values_list('grade_score_int',flat=True))),2)) for a in sub_list_counter]

        course_params = {
            'form':form,
            'sub_list_counter':sub_list_counter,
            'zenkari_ranking':zenkari_ranking,
        }
        return render(request, 'gv/course.html', course_params)


    sub_list = sub_obj.values_list('subjectname', flat=True)#授業名でリストを取得(重複あり)


    #pagenationがうまくいかないため今だけ変更
    sub_list_counter = Counter(sub_list).most_common()[:50] #授業の数(多い順)

    #変更された1行(読みずらいが高速)
    sub_list_counter = [(a[0],a[1],np.round(np.average(list(sub_obj.filter(subjectname=a[0]).values_list('grade_score_int',flat=True))),2),sub_obj.filter(subjectname=a[0])[0].category1) for a in sub_list_counter]
    #gpa順にソートしたリスト
    sub_list_counter_sorted_gpa = sorted(sub_list_counter, key=lambda sub_list_counter: sub_list_counter[2], reverse=True)

    form = find_course()
    make_list('category1','category1',sn,form)
    now_field = form.fields['category1'].choices
    #選択肢から必修を取り除く
    new_field = [e for e in now_field if '必' not in e[1]]
    form.fields['category1'].choices = new_field
    course_params = {
        'gakka':gg_lists[sn[2:4]],
        'sub_obj':sub_obj,
        'form':form,
        #'sub_list_counter':sub_list_counter,
        'category1_list_course':category1_list_course,
        'sub_list_counter':sub_list_counter,
        'sub_list_counter_sorted_gpa':sub_list_counter_sorted_gpa,
        'zenkari_ranking':zenkari_ranking,
        'zenkari_ranking_sorted_gpa':zenkari_ranking_sorted_gpa,
        }
    return render(request, 'gv/course.html', course_params)

#########################################################################
                            #授業分析(11月27日)new!!!
#########################################################################
def sub_search(request):


    all_sub_list = list(set(subjectInfo.objects.values_list('subjectname', flat=True)))#すべての授業のリスト(重複なし)
    try:#sessionが切れていないか確認
        sn = request.session['stunum']  #学籍番号をsessionから持ってくる
    except:
        numbers = request.session['numbers']
        form = userInfoForm()
        hp_params = {
            'form':form,
            'message':'学籍番号とパスワードを入力しよう',
            'numbers':numbers,

            }
        return render(request, 'gv/hp.html', hp_params)
    if request.method == 'POST':
        form = find_sub(request.POST)
        s_name = request.POST['s_name']

        sub_obj = subjectInfo.objects.filter(subjectname=s_name)


        #num_sub = len(sub_obj)#その先生の授業数
        grade_list_dict = OrderedDict({'Ｓ':0,'Ａ':0,'Ｂ':0,'Ｃ':0}) #順番がたぶん大事
        grade_list = sub_obj.values_list('grade', flat=True)#成績判定を取得(重複あり)
        grade_list_dict_new = Counter(grade_list) #授業の数
        grade_list_dict.update(grade_list_dict_new) #辞書をupdate
        nums = grade_list_dict.values()
        nums = list(nums)#リストにする
        grade_list_sample = list(grade_list_dict.keys())
        #'履を履修中に変更'
        for i in range(len(grade_list_sample)):
            if grade_list_sample[i]=="履":
                grade_list_sample[i]="履修中"
            if grade_list_sample[i] == 'Q':
                grade_list_sample[i] == '履修中止'

        #その授業のGPA

        s_gpa = list(sub_obj.exclude(grade__contains='履').exclude(grade='Q').values_list('grade_score_int', flat=True))
        #s_gpa = s_gpa.exclude(grade__contains='履')
        #s_gpa = np.round(np.sum(s_gpa)/len(s_gpa),2)
        s_gpa = np.round(np.average(s_gpa),2)


        #その授業の先生のリスト
        t_list = list(sub_obj.values_list('teacher',flat=True))
        t_list = [a.replace('\u3000', '　') for a in t_list]
        t_dict = Counter(t_list).most_common()
        len_t_dict = len(t_list)
        t_dict = [(a[0],np.round(a[1]/len_t_dict*100,1)) for a in t_dict]#先生名、担当率
        ##################### 11/28 new added 先生名でDB検索し、単位取得済みの評価平均を数値化（GPA化）
        t_dict_message01 = np.array(t_dict)
        np_t_list = t_dict_message01[:,0]

        zgpa = []
        for i in range(len(np_t_list)):
            teacher_name = np_t_list[i]
            zyugyo_gpa = list(sub_obj.filter(teacher=teacher_name).values_list('grade_score_int', flat=True).exclude(grade__contains='履'))
            zgpa_ave=np.round(np.sum(zyugyo_gpa)/len(zyugyo_gpa),2)
            zgpa.append(zgpa_ave)
        t_dict_message2 = np.array(zgpa)
        t_dict_message2=np.reshape(t_dict_message2, (t_dict_message2.shape[0], 1))
        t_dict = np.hstack([t_dict_message01,t_dict_message2])

        sub_search_params = {
            't_dict':t_dict,
            'form':form,
            #'sub_obj':sub_obj,
            'nums':nums,
            'grade_list_sample':grade_list_sample,
            'all_sub_list':all_sub_list,
            #'teacher_sub_dict':teacher_sub_dict,
            'r_form':'{}'.format(s_name).replace('　',''),
            's_gpa':s_gpa,
        }

        return render(request, 'gv/sub_search.html', sub_search_params)

    form = find_sub()
    nums = [0,0,0,0,0]
    grade_list_sample = ['S','A','B','C','D']
    sub_search_params = {
        'all_sub_list':all_sub_list,
        'nums':nums,
        'grade_list_sample':grade_list_sample,
        'r_form':'授業分析',
        'form':form,
    }
    return render(request, 'gv/sub_search.html', sub_search_params)

def sirabasu(request):
    sub_name=request.POST['sub-name']#授業名を取得
    ################## 11/28 new added #################
    try:#特殊授業以外はうまくいく想定
        subinfo = subjectInfo.objects.filter(subjectname=sub_name)[0]#データベースから該当する授業を取得
    except:# ゼミナール　Aなどの時エラー回避
        url = 'https://sy.rikkyo.ac.jp/timetable/slbsskgr.do'
        return HttpResponseRedirect('{}'.format(url))
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

def more(request):
    input_t_name_true = request.GET.get('name')
    sub_list = list(subjectInfo.objects.filter(teacher=input_t_name_true).values_list('subjectname', flat=True))
    sub_list_unique = list(set(sub_list))


    more_params = {
        'sub_list':sub_list,
        'sub_list_unique':sub_list_unique,
    }
    return render(request, 'gv/more.html', more_params)

def teacher_search(request):

    try:#sessionが切れていないか確認
        sn = request.session['stunum']  #学籍番号をsessionから持ってくる
    except:
        numbers = request.session['numbers']
        form = userInfoForm()
        hp_params = {
            'form':form,
            'message':'学籍番号とパスワードを入力しよう',
            'numbers':numbers,

            }
        return render(request, 'gv/hp.html', hp_params)
    import time
    start = time.time()##########################
    sub_obj = subjectInfo.objects.all()
    teacher_list_space = list(set(subjectInfo.objects.values_list('teacher', flat=True)))#すべての先生のリスト(重複なし)
    #teacher_list = [i.replace('　', '') for i in teacher_list_space]#先生の名前スペースなし
    #各先生の授業のリストを生成(ex:{'A先生':[B,C,D]})
    #teacher_sub_dict = {teacher_name.replace('　', ''):list(set(subjectInfo.objects.filter(teacher__contains=teacher_name).values_list('subjectname', flat=True))) for teacher_name in teacher_list_space}

    if request.method == 'POST':
        form = find_teacher(request.POST)
        t_name = request.POST['t_name']
        t_sub = request.POST['t_sub']

        sub_obj = sub_obj.filter(teacher=t_name)
        #授業のフィルター
        if len(t_sub) is not 0:
            sub_obj = sub_obj.filter(subjectname=t_sub)

        #num_sub = len(sub_obj)#その先生の授業数
        grade_list_dict = OrderedDict({'Ｓ':0,'Ａ':0,'Ｂ':0,'Ｃ':0}) #順番がたぶん大事
        grade_list = sub_obj.values_list('grade', flat=True)#成績判定を取得(重複あり)
        grade_list_dict_new = Counter(grade_list) #授業の数
        grade_list_dict.update(grade_list_dict_new) #辞書をupdate
        nums = grade_list_dict.values()
        nums = list(nums)#リストにする
        grade_list_sample = list(grade_list_dict.keys())
        for i in range(len(grade_list_sample)):
            if grade_list_sample[i]=="履":
                grade_list_sample[i]="履修中"

        ################# 11/28 new added その先生のGPA
        zyugyo_gpa = list(sub_obj.filter(teacher=t_name).values_list('grade_score_int', flat=True).exclude(grade__contains='履'))
        k_gpa = np.round(np.sum(zyugyo_gpa)/len(zyugyo_gpa),2)

        ######################################
        elapsed_time = time.time() - start
        teacher_search_params = {
            'elapsed_time':elapsed_time,
            'message':'ok,',
            'form':form,
            'sub_obj':sub_obj,
            'nums':nums,
            'grade_list_sample':grade_list_sample,
            'teacher_list_space':teacher_list_space,
            #'teacher_sub_dict':teacher_sub_dict,
            'r_form':'{}  {}'.format(t_name,t_sub).replace('　',''),
            'k_gpa':k_gpa,
        }

        return render(request, 'gv/teacher_search.html', teacher_search_params)

    form = find_teacher()
    nums = [0,0,0,0,0]
    grade_list_sample = ['S','A','B','C','D']

    #elapsed_time = time.time() - start
    teacher_search_params = {
        #'elapsed_time':elapsed_time,
        'message':'',
        'form':form,
        'nums':nums,
        'grade_list_sample':grade_list_sample,
        'teacher_list_space':teacher_list_space,
        #'teacher_sub_dict':teacher_sub_dict,
        'r_form':'成績判定統計',
    }

    return render(request, 'gv/teacher_search.html', teacher_search_params)

#####################################################################################
                            #フォームを人それぞれで分ける 関数化
#####################################################################################
def make_list(model_name,form_name,sn,form):
    kind_list = list(set(list(subjectInfo.objects.filter(user_id=sn).values_list('{}'.format(model_name), flat=True))))
    the_field = form.fields['{}'.format(form_name)]
    form_list = [('','{}'.format(form_name))]
    for i in range(0, len(kind_list)):
        form_tuple = (kind_list[i],kind_list[i])
        form_list.append(form_tuple)
        the_field.choices = form_list
    return


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                                                                        #その他
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def pastdata(request):
    form = userInfoForm()
    stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
    numbers=len(stuobj)

    try:#sessionが切れていないか確認
        sn = request.session['stunum']  #学籍番号をsessionから持ってくる
        #同学科の１つ先輩の学籍番号をリスト化
        targets = list(studentInfo.objects.filter(user_id__contains=str(int(sn[0:2])-1)+str(sn[2:4])).values_list('user_id', flat=True))
        if len(targets)==0:
            senpai_data_list = ['データなし','','','','']
            pastdata_params = {
                'form':form,
                'message':'',
                'data':senpai_data_list,
                'numbers':numbers,
                }
            return render(request, 'gv/pastdata.html', pastdata_params)
        udatas = []
        for k in range(len(targets)):
            #個人の成績データを抽出するコード
            tgt = subjectInfo.objects.filter(user_id__contains=str(targets[k]))
            #必要な項目ごとに個人データを取り出す
            subname, catename, tname, haruaki, nendo = list(tgt.values_list('subjectname',flat=True)),list(tgt.values_list('category1',flat=True)),list(tgt.values_list('teacher',flat=True)),list(tgt.values_list('season',flat=True)),list(tgt.values_list('year_int',flat=True))
            #個人データの二次元配列リストを作る
            tgtdata = []
            for i in range(len(subname)):
                name = str(tname[i])
                sub = str(subname[i])
                if "\u3000" in name:
                    name = name.replace("\u3000"," ")
                if "\u3000" in sub:
                    sub = sub.replace("\u3000"," ")
                data = [sub,catename[i],name,haruaki[i],nendo[i]]
                tgtdata.append(data)
            newl = []
            nen = np.array(sorted(list(set(np.array(tgtdata)[:,4])),reverse=True))[0:2] #先輩の最も新しい成績年度の数字　2018とか
            for i in range(len(subname)): #最も新しい年度のデータのみを先ほど作ったリストから抽出
                if np.array(tgtdata)[i,4] == nen[0] or np.array(tgtdata)[i,4] == nen[1]:
                    newl.append(list(np.array(tgtdata)[i]))
            
            udf = pd.DataFrame(sorted(newl,key=itemgetter(4,3),reverse=True))
            udf.columns = ['subject','category','teacher','haruaki','nendo']
            udatas.append(udf)

        senpai_data_list = (udatas[np.random.randint(len(udatas))]).values.tolist()

        pastdata_params = {
            'form':form,
            'message':'',
            'data':senpai_data_list,
            'numbers':numbers,
            }
        return render(request, 'gv/pastdata.html', pastdata_params)
        
    except:
        index_params = {
            'form':form,
            'message':'',
            'numbers':numbers,
            }

        return render(request, 'gv/hp.html', index_params)




####################################################################################
                                #利用者の詳細を確認するためのカウンター
####################################################################################
def counter(request):
    #sn = request.session['stunum']  #学籍番号をsessionから持ってくる
    form = ggs_counter_Form()
    ######
    stuobj = list(studentInfo.objects.values_list('user_id', flat=True))
    numbers=len(stuobj)   #　↓　利用者の入学年度を重複を省いてリスト化 →　[17, 16, 15]　こんな感じになる
    list_y = sorted([int(str(list(set(studentInfo.objects.values_list('enteryear', flat=True)))[i])[2:4]) for i in range(len(list(set(studentInfo.objects.values_list('enteryear', flat=True)))))],reverse=True)
    users_by_year = [(i,len(studentInfo.objects.filter(user_id__startswith=i))) for i in list_y]#学年別利用者人数を動的に生成　⇒　[(17, 1), (16, 7), (15, 1)]　こんな感じになる
    #####
    gg_lists = {'aa':'キリスト教学科','ac':'史学科','ae':'教育学科','am':'文学科{英米文学専修}','an':'文学科{ドイツ文学専修}','as':'文学科{フランス文学専修}','at':'文学科{日本文学専修}','au':'文学部{文芸・思想専修}','ba':'経済学科','bc':'会計ファイナンス学科','bd':'経済政策学科','bm':'経営学科','bn':'国際経営学科','ca':'数学科','cb':'物理学科','cc':'化学科','cd':'生命理学科','da':'社会学科','dd':'現代文化学科','de':'メディア社会学科','dm':'異文化コミュニケーション学科','ea':'法学科','ec':'政治学科','ed':'国際ビジネス法学科','ib':'福祉学科','ic':'コミュニティ政策学科','id':'スポーツウエルネス学科','hm':'心理学科','hn':'映像身体学科','ha':'観光学科','hb':'交流文化学科'}
    #  ↓　　表の中身のパラメータを生成
    ggobj = [(key,gg_list,len(studentInfo.objects.filter(user_id__contains=gg_list)),np.round(np.average(sorted(list(studentInfo.objects.filter(user_id__contains=gg_list).values_list('gpa', flat=True)),reverse=True)),2)) for gg_list,key in gg_lists.items()]
    ggobj.sort(key=itemgetter(2),reverse=True)#履修者数順
    ggobj2 = sorted(ggobj,key=itemgetter(3,2),reverse=True)#GPA順且つ履修者も降順

    if request.method == 'POST':
        gg_name = request.POST['gg_name']
        gakunenn = request.POST['gakunenn']
        ggs_numbers = len(studentInfo.objects.filter(user_id__contains=gg_name))
        # フォームで指定された条件のgpa平均を出す
        gpa_ave = np.average(sorted(list(studentInfo.objects.filter(user_id__contains=gg_name).values_list('gpa', flat=True)),reverse=True))
        if gakunenn == 0:
            pass
        else:
            gg_name=str(gakunenn)+str(gg_name)
            ggs_numbers = len(studentInfo.objects.filter(user_id__contains=gg_name))
            #gpa平均を出す
            gpa_ave = np.average(sorted(list(studentInfo.objects.filter(user_id__contains=gg_name).values_list('gpa', flat=True)),reverse=True))
    else:
        ggs_numbers, gakunenn, gpa_ave = [0,0,0]
    gpa_ave=np.round(gpa_ave,2)
    #####
    counter_params={
        'form':form,
        'ggs_numbers':ggs_numbers,
        'gakunenn':gakunenn,
        'gpa_ave':gpa_ave,
        'ggobj_counter':ggobj,
        'ggobj_counter2':ggobj2,
        'numbers':numbers,
        'users_by_year':users_by_year,
    }
    return render(request,'gv/counter.html',counter_params)



###################################################################################
                                    #about usのところ
#################################################################################
def inquiry(request):
    inquiry_params = {}
    return render(request, 'gv/inquiry.html', inquiry_params)








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


###################################################################################
                                    #停止
##################################################################################
