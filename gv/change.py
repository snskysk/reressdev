
def pytojsMaterials(result, list_pie, list_bar, table, kyoushoku_c):
    #必要ライブラリのimport
    import re

    #戻り値の辞書
    params = {}


    #ローマ字で名前の取得
    #データフレームの名前部分の取得()
    name = result[0].iloc[2,2]
    str_name = ''
    alnumReg = re.compile(r'^[a-zA-Z0-9]+$')
    #文字列が英数字のみであったらtrueを返す関数
    def isalnum(s):
        return alnumReg.match(s) is not None
    #name(名前)から英語部分のみを返す
    for i in name:
        if isalnum(i):
            str_name = str_name + i
    #returnMaterial.append(str_name)
    params['str_name'] = str_name

    #現時点での累計gpaの取得
    gpa = list(result[1]['累計'])[-1]
    params['gpa'] = gpa

    #単位の取得率(ex:専門選択の取得パーセンテージ)
    Achivement_list = list(list_bar[2]['現在達成率(%)'])
    Aciecement_list = [100 if i > 100 else i for i in Achivement_list]#100以上は100にする。

    params['Achivement_list'] = Achivement_list
    #str_Achievement_list = str(Achivement_list)[1:-2]
    #params['str_Achievement_list'] = str_Achievement_list

    #単位の種類のリスト
    kind_name = list(list_bar[2].index)
    #文字列を取得しシングルクォーテーションを消す
    str_kind_name = str(kind_name)[1:-2].replace("'","")
    #※マークを消すための2行
    kome = str_kind_name[0]
    str_kind_name = str_kind_name.replace(kome,'')
    kind_name = str_kind_name.split(',')
    #params['str_kind_name'] = str_kind_name
    params['kind_name'] = kind_name
    #print(params['kind_name'])


    #円グラフ(S,A,B,C,Dの比率)
    unitOfcircle, gradeOfcircle = list_pie[4:6]
    params['unitOfcircle'] = unitOfcircle
    params['gradeOfcircle'] = gradeOfcircle


    #########################棒グラフ用データ#######################################
    #不足単位数と履修単位数
    lb1, lb2 = list_bar[0:2]
    ##残単を計算する
    import numpy as np
    #マイナスがある場合は0にする。

    residual_unit = list(np.array(lb1['必要単位数']) - np.array(lb1['修得単位数']))

    on_course = list(lb2['履修単位数'])

    #残単位と履修単位がどちらも0の場合は表示しない(消す)
    bou_data_old = np.array([kind_name,residual_unit,on_course])#もともとのデータ
    bou_data = np.array([residual_unit,on_course])#単位の種類を抜いた行列(数値のみ)
    #bou_data_zero = np.array(np.where(np.sum(bou_data, axis=0)== 0))[0]#(行に対しての和が0になる列のmask)
    bou_data_zero = np.array(np.where(np.sum(bou_data, axis=0) <= 0))[0]#(行に対しての和が0になる列のmask)
    list_bou_data_zero = list(bou_data_zero)
    bou_data_new = np.delete(bou_data_old,list_bou_data_zero,1)#maskをかけていらない列を消す


    #随意科目などをとっていた場合の処理(-の場合0にする)
    #residual_unit_bou = list(bou_data_new[1])
    #residual_unit_bou = [0 if i < 0 else i for i in list(bou_data_new[1])]

    params['kind_name_bou'] = list(bou_data_new[0])
    params['residual_unit_bou'] = list(bou_data_new[1])
    #params['residual_unit_bou'] = r
    params['on_course_bou'] = list(bou_data_new[2])


    #ドーナッツグラフ用
    residual_num = np.sum(np.array(list_bar[1]['不足単位数']))
    get_num = np.sum(np.array(lb1['修得単位数']))-kyoushoku_c#修得単位数
    on_num = list_pie[6][6] - get_num -residual_num#list_pie[6][6]は必要単位数
    #もし必要単位を超えていたら修正
    if get_num > list_pie[6][6]:
        get_num = list_pie[6][6]
        on_num = 0
    params['residual_num'] = residual_num
    params['on_num'] = on_num
    params['get_num'] = get_num

    return params


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
            result, list_pie, list_bar, table, personal_dataset, kyoushoku_c, passcheck = condact(value)
            if passcheck==1:
                pass
            elif passcheck==2:
                form = userInfoForm()
                index_params = {
                'form':form,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ２'
                }
                return render(request, 'gv/hp.html', index_params)

            elif passcheck==3:
                form = userInfoForm()
                index_params = {
                'form':form,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ３'
                }
                return render(request, 'gv/hp.html', index_params)

            elif passcheck==4:
                form = userInfoForm()
                index_params = {
                'form':form,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ４'
                }
                return render(request, 'gv/hp.html', index_params)

            elif passcheck==5:
                form = userInfoForm()
                index_params = {
                'form':form,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ５'
                }
                return render(request, 'gv/hp.html', index_params)

            elif passcheck==11:
                form = userInfoForm()
                index_params = {
                'form':form,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ１１'
                }
                return render(request, 'gv/hp.html', index_params)
            elif passcheck==12:
                form = userInfoForm()
                index_params = {
                'form':form,
                'message':'データ加工に失敗しました。対応していないユーザーである可能性があります。エラータイプ：フェーズ１２'
                }
                return render(request, 'gv/hp.html', index_params)

            else:
                form = userInfoForm()
                index_params = {
                'form':form,
                'message':'学生番号かパスワードが間違っている可能性があります'
                }
                return render(request, 'gv/hp.html', index_params)         #正しくなかったら戻る
        except Exception as e:
            form = userInfoForm()
            index_params = {
            'form':form,
            'message':'お手数ですが、再度お試しください。それでもご利用になれない場合は、よろしければ学年と学部学科、特殊な授業の履修履歴などがあれば明記の上お問い合わせください。'
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
