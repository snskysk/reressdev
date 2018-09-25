from django.shortcuts import render, redirect
from .forms import userInfoForm, findForm
from .models import studentInfo, subjectInfo
import main
from pytojs import pytojsMaterials
# Create your views here.
def index(request):
    form = userInfoForm()
    params = {
        'form':form,
        'message':'学籍番号とパスワードを入力してね',
        }

    return render(request, 'gv/index.html', params)


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
            params = {
            'form':form,
            'message':'学籍番号かパスワードがまちがえてるよ♡<br>\
            もう一度入力してね♡'
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
