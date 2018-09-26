
# coding: utf-8

# In[2]:


# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import getpass
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import os
#from PIL import Image
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#from matplotlib.font_manager import FontProperties



def func1(value):
    USER=value[0]
    PASS=value[1]
    URL="https://rs.rikkyo.ac.jp/"

    time.sleep(1)
    print("---Chromeを起動---")

    #options = Options()
    # Heroku以外ではNone
    #if chrome_binary_path: options.binary_location = chrome_binary_path
    #options.add_argument('--headless')
    #driver = Chrome(executable_path=driver_path, chrome_options=options)

    # ここでchrome_binary_locationを指定
    #CHROME_BINARY_LOCATION='/app/.apt/opt/google/chrome/google-chrome'
    GOOGLE_CHROME_SHIM= '/app/.apt/opt/google/chrome/google-chrome'

    #chrome_options = Options()
    #chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"
    #chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument('--no-sandbox')
    #driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)

    chrome_bin = os.environ.get(GOOGLE_CHROME_SHIM, None)
    opts = Options()
    opts.binary_location = chrome_bin
    Options.add_argument('--headless')
    Options.add_argument('--disable-gpu')
    Options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=opts)

    #driver = webdriver.Chrome(executable_path='Chromedriverがあるパス')
    #options = Options()
    #options.add_argument('--headless')
    #driver = webdriver.Chrome(chrome_options=options)

    try:
        print("---https://rs.rikkyo.ac.jp/にアクセス---")
        driver.get(URL)

        print("---ユーザ情報を入力---")
        driver.find_element_by_css_selector("#userNameInput").send_keys(USER)
        driver.find_element_by_css_selector("#userNameInput").send_keys(Keys.RETURN)

        driver.find_element_by_css_selector("#passwordInput").send_keys(PASS)
        driver.find_element_by_css_selector("#passwordInput").send_keys(Keys.RETURN)
        print("---ユーザ情報入力完了　―　ページ遷移---")

        time.sleep(1)

        #print("---スクリーンショットの保存---")
        #driver.save_screenshot("gv/static/gv/images/test101.png")

        print("---ページ遷移---")
        driver.find_element_by_css_selector("#MainContent_Contents_MenuCtrl_lnkSeiseki").click()


        print("---ページソースを取得---")
        html=driver.page_source

        print("---ページソースからテーブル要素を取得---")
        tables = pd.io.html.read_html(html, flavor='bs4')
        print("---全"+str(len(tables))+"個のテーブルを取得---")

        time.sleep(1)


        driver.close()
        print("---Chromeをダウン---")
        print("---process all complete---")
        print("--------------------------")

    except:
        driver.quit()
        print('error確認!chromeを閉じるよ')

    zen=["Ｓ","Ａ","Ｂ","Ｃ"]
    #user_info=tables[2]
    #unit_info=tables[3]
    #gpa_info=tables[4]
    #grade_info=tables[6]

    user_info=tables[2]
    unit_info=tables[4]
    gpa_info=tables[5]
    grade_info=tables[7]

    user_info.columns=['Major&Grade', 'ID&Class', 'userName', 'enterYear', 'seasons']

    unit_info.columns = ['区分名', '必要単位数', '修得単位数', '履修単位数', '不足単位数', '備考']
    main_unit=unit_info.query("index!=0&index!=1")

    gpa_info.columns=["年度","春学期","秋学期","年度計","累計"]


    # 成績データにcolomnsを付与
    grade_info.columns = ['Num', 'subjectnum', 'subjectname', 'unit', 'grade', 'year', 'season','teacher','etcA','managementnum']

    # 主要データのみを抽出してデータフレームを作る
    main_GI=grade_info[['subjectnum','subjectname', 'unit', 'grade', 'year', 'season','teacher','managementnum']]

    # 成績データのアルファベットから数値への変換
    grade_info_grade=main_GI[["grade"]]
    grade_info_gradenp=np.array(grade_info_grade)
    grade_score=[]
    for s in range(len(grade_info_gradenp)):
        if grade_info_gradenp[s,0]=="Ｓ":
            grade_score.append("4")
        elif grade_info_gradenp[s,0]=="Ａ":
            grade_score.append("3")
        elif grade_info_gradenp[s,0]=="Ｂ":
            grade_score.append("2")
        elif grade_info_gradenp[s,0]=="Ｃ":
            grade_score.append("1")
        else:
            grade_score.append("NaN")

    grade_score=np.array(grade_score)
    grade_score=pd.DataFrame({
        "grade_score":grade_score
    })
    main_GI=pd.concat([main_GI,grade_score],axis=1)

    math_score=np.array(main_GI[["unit","grade_score"]])
    math_score
    result_score=[]
    for s in range(len(math_score)):
        if math_score[s,1]=="1":
            math=np.array(math_score[s].astype(int))
            math=math[0]*math[1]
            math=math.astype(object)
            result_score.append(math)
        elif math_score[s,1]=="2":
            math=np.array(math_score[s].astype(int))
            math=math[0]*math[1]
            math=math.astype(object)
            result_score.append(math)
        elif math_score[s,1]=="3":
            math=np.array(math_score[s].astype(int))
            math=math[0]*math[1]
            math=math.astype(object)
            result_score.append(math)
        elif math_score[s,1]=="4":
            math=np.array(math_score[s].astype(int))
            math=math[0]*math[1]
            math=math.astype(object)
            result_score.append(math)
        else:
            result_score.append("NaN")

    result_score=np.array(result_score)
    result_score=pd.DataFrame({
        "result_score":result_score
    })

    main_GI=pd.concat([main_GI,result_score],axis=1)

    npmain_GI=np.array(main_GI)

    gpa_np=np.array(gpa_info.query('index!=0 & index!=1')[["累計"]])
    gpa_np=gpa_np[len(gpa_np)-1,0]
    gpa_np

    gpa_data=[]
    for s in range(len(npmain_GI)):
        if npmain_GI[s,3]==zen[0]:
            gpa_data.append(gpa_np)

        elif npmain_GI[s,3]==zen[1]:
            gpa_data.append(gpa_np)

        elif npmain_GI[s,3]==zen[2]:
            gpa_data.append(gpa_np)

        elif npmain_GI[s,3]==zen[3]:
            gpa_data.append(gpa_np)
        else:
            gpa_data.append("NaN")

    gpa_data=np.array(gpa_data)
    gpa_data=pd.DataFrame({
        "gpa_data":gpa_data
    })


    main_GI=pd.concat([main_GI,gpa_data],axis=1)

    npsN=np.array(main_GI[["subjectname"]])
    mgt5=main_GI.query('subjectname.astype("str").str.contains("＊") or subjectname.astype("str").str.contains("◆")',engine="python")[["subjectname"]]
    mgt5index=mgt5.index
    mgt5index=np.array(mgt5index)
    mgt5index_count=len(mgt5index)

    category1=[]

    s=0
    k=0
    for i in range(len(main_GI)):
        if npsN[s,0]==npsN[mgt5index[k],0]:
            if k<len(mgt5index)-1:
                for p in range(mgt5index[k+1]-mgt5index[k]):
                    category1.append(npsN[mgt5index[k],0])
                    s+=1
                k+=1
            else:
                for p in range(100):
                    category1.append(npsN[mgt5index[k],0])
                    s+=1
                    if s==len(main_GI):
                        break
        else:
            category1.append("NaN")
            s+=1
        if s==len(main_GI):
            break

    category1=np.array(category1)
    category1=pd.DataFrame({
        "category1":category1
    })

    main_GI=pd.concat([main_GI,category1],axis=1)


    npsN=np.array(main_GI[["subjectname"]])
    mgt6=main_GI.query('subjectname.astype("str").str.contains("◆")',engine="python")[["subjectname"]]
    mgt6index=mgt6.index
    mgt6index=np.array(mgt6index)
    mgt6index_count=len(mgt6index)

    category2=[]

    s=0
    k=0
    for i in range(len(main_GI)):
        if npsN[s,0]==npsN[mgt6index[k],0]:
            if k<len(mgt6index)-1:
                for p in range(mgt6index[k+1]-mgt6index[k]):
                    category2.append(npsN[mgt6index[k],0])
                    s+=1
                k+=1
            else:
                for p in range(100):
                    category2.append(npsN[mgt6index[k],0])
                    s+=1
                    if s==len(main_GI):
                        break
        else:
            category2.append("NaN")
            s+=1
        if s==len(main_GI):
            break

    category2=np.array(category2)
    category2=pd.DataFrame({
        "category2":category2
    })


    main_GI=pd.concat([main_GI,category2],axis=1)

    # unitの値（1か2か4しか持たないため）を利用して必要な行のみを抽出したデータフレームを作る
    sub1_GI=main_GI.query('unit=="1"|unit=="2"|unit=="4"|unit=="6"|unit=="8"')
    sub1_GI

    columns01=np.array(sub1_GI.columns)

    kyoushoku_c=len(sub1_GI.query('category2.astype("str").str.contains("講座科目")',engine="python"))

    if kyoushoku_c>0:
        kyoushokunp=np.array(sub1_GI)
        a=kyoushokunp[0:((len(sub1_GI.index))-kyoushoku_c),:]
        b=kyoushokunp[((len(sub1_GI.index))-kyoushoku_c+1):(len(sub1_GI.index)),:]

        sub2_GI=pd.DataFrame({
        columns01[0]:a[:,0]
        })
        for i in range(len(columns01)-1):
            sub3_GI=pd.DataFrame({
            columns01[1+i]:a[:,1+i]
            })

            sub2_GI=pd.concat([sub2_GI,sub3_GI],axis=1)

        sub4_GI=pd.DataFrame({
        columns01[0]:a[:,0]
        })
        for i in range(len(columns01)-1):
            sub5_GI=pd.DataFrame({
            columns01[1+i]:a[:,1+i]
            })

            sub4_GI=pd.concat([sub4_GI,sub5_GI],axis=1)
        allGI=sub1_GI
        sub1_GI=sub2_GI
        sub2_GI=sub4_GI
    else:
        pass

    # cl1=columns-list-1
    cl1= ['区分名', '必要単位数', '修得単位数', '履修単位数', '不足単位数', '備考']

    # 区分名のデータフレームを行列に変換
    class_U=main_unit[cl1[0]]
    class_Unp=np.array(class_U)
    class_Unp

    # objectをintにして、さらにデータフレームをnumpy.ndarray型に変換
    must_U=np.array(main_unit[cl1[1]].astype(int))
    got_U=np.array(main_unit[cl1[2]].astype(int))
    present_U=np.array(main_unit[cl1[3]].astype(int))
    lack_U=np.array(main_unit[cl1[4]].astype(int))

    # 現在達成率（不足単位数に対する修得単位数の割合）と予定達成率（不足単位数に対する修得単位数と現在履修単位数の和の割合）の算出
    # 予定達成率は、今期順当に単位をとれたとした場合の達成率
    present_rate,future_rate=[],[]
    for i in range(len(class_Unp)):
        if must_U[i]==0:
            a=0
            present_rate.append(a)
            future_rate.append(a)
        else:
            present_rate.append(got_U[i]/must_U[i]*100)
            future_rate.append((got_U[i]+present_U[i])/must_U[i]*100)

    present_rate=np.array(present_rate)
    future_rate=np.array(future_rate)

    #結合のために、一次元配列を二次元配列に再加工
    list2=[must_U,got_U,present_rate,future_rate,lack_U,class_Unp,present_U]
    must_U=np.reshape(list2[0], (list2[0].shape[0], 1))
    got_U=np.reshape(list2[1], (list2[1].shape[0], 1))
    present_rate=np.reshape(list2[2], (list2[2].shape[0], 1))
    future_rate=np.reshape(list2[3], (list2[3].shape[0], 1))
    lack_U=np.reshape(list2[4], (list2[4].shape[0], 1))
    class_Unp=np.reshape(list2[5], (list2[5].shape[0], 1))
    present_U=np.reshape(list2[6], (list2[6].shape[0], 1))

    # 生成データは、'必要単位数', '修得単位数'、現在達成率、予定達成率、不足単位数,'区分名', '履修単位数'
    main_Unprm=np.concatenate([must_U,got_U,present_rate,future_rate,lack_U,class_Unp,present_U],axis=1)

    list3=['必要単位数', '修得単位数',"現在達成率(%)","予定達成率(%)","不足単位数",'区分名','履修単位数']
    m_U=main_Unprm
    main_Updrm=pd.DataFrame({
        list3[0]:m_U[:,0],
        list3[1]:m_U[:,1],
        list3[2]:m_U[:,2],
        list3[3]:m_U[:,3],
        list3[4]:m_U[:,4],
        list3[5]:m_U[:,5],
        list3[6]:m_U[:,6]

    })
    df_rm=main_Updrm.loc[:,('区分名','必要単位数', '修得単位数','履修単位数',"不足単位数","現在達成率(%)","予定達成率(%)")]
    df_rm


    result=[user_info,gpa_info,df_rm,sub1_GI,main_unit]
    return result
