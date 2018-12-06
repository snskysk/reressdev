
# coding: utf-8

# In[14]:


# 円ブラフのでデータセットを返す関数
def piegraph_dataset(tables,passcheck):

    import numpy as np
    import pandas as pd

    user_info=tables[0]
    gpa_info=tables[1]
    df_rm=tables[2]
    sub1_GI=tables[3]
    main_unit=tables[4]

    # 学年と入学年度を変数化   by   user_info
    userGrade=user_info.query("index==3")[["Major&Grade"]]
    userGrade=np.array(userGrade.astype(int))
    enterYear=user_info.query("index==2")[["enterYear"]]
    enterYear=np.array(enterYear.astype(int))
    userGrade=userGrade[0,0]

    # 成績表の科目合計を返す
    subject_total=len(sub1_GI[["unit"]])

    main_gpa=gpa_info.query('index!=0 & index!=1')[["累計"]]
    npm_gpa=np.array(main_gpa.astype(float))
    gpa_value=npm_gpa[len(npm_gpa)-1,0]

    #　2015年以前入学者との場合分け　gpaは0としてあるため、0と一致した場合Dは0にしておく
    if passcheck==401:
        score_D=0
    else:

        for_D=sub1_GI.query('grade=="Ｓ"|grade=="Ａ"|grade=="Ｂ"|grade=="Ｃ"')[["unit","result_score"]]
        for_D=(np.array(for_D.astype(int)))
        for i in range(150):
            for_D1=np.sum(for_D[:,1])
            for_D0=np.sum(for_D[:,0])
            if np.round((for_D1/(for_D0+i)),2)==gpa_value:
                score_D=i
                break
            else:
                pass
        score_D

    # 円グラフ用データの前処理
    zen=["Ｓ","Ａ","Ｂ","Ｃ"]
    if passcheck==401:
        data,label,dfdata,dflabel=[1,1,1,1]
    else:
        # graph1
        grade_S=len(sub1_GI.query('grade=="Ｓ"'))
        grade_A=len(sub1_GI.query('grade=="Ａ"'))
        grade_B=len(sub1_GI.query('grade=="Ｂ"'))
        grade_C=len(sub1_GI.query('grade=="Ｃ"'))
        grade_Q=len(sub1_GI.query('grade=="Ｑ"'))

        data=[grade_S,grade_A,grade_B,grade_C,grade_Q]
        label=["S","A","B","C","stop"]

        dfdata=[grade_S,grade_A,grade_B,grade_C,grade_Q]
        dflabel=["S","A","B","C","履修中止"]
        totalscore=0
        for s in dfdata:
            totalscore=totalscore+s
        dfdata.append(totalscore)
        dflabel.append("total")

    # number2pie-graph
    score_S=np.array(sub1_GI.query('grade=="Ｓ"')[["unit","grade_score"]].astype(int))
    score_S=np.sum(score_S[:,0])
    score_A=np.array(sub1_GI.query('grade=="Ａ"')[["unit","grade_score"]].astype(int))
    score_A=np.sum(score_A[:,0])
    score_B=np.array(sub1_GI.query('grade=="Ｂ"')[["unit","grade_score"]].astype(int))
    score_B=np.sum(score_B[:,0])
    score_C=np.array(sub1_GI.query('grade=="Ｃ"')[["unit","grade_score"]].astype(int))
    score_C=np.sum(score_C[:,0])

    score_data=[score_S,score_A,score_B,score_C,score_D]
    score_label=["S","A","B","C","D"]


    totalscore=0
    for s in range(len(score_data)-1):
        k=score_data[s]
        totalscore=totalscore+k

    mustscore=np.array(main_unit[["必要単位数"]].astype(int))
    mustscore=np.sum(mustscore)

    lackscore=mustscore-totalscore

    dfscore_data=[score_S,score_A,score_B,score_C,score_D,totalscore,mustscore,lackscore]
    dfscore_label=["S","A","B","C","D","取得単位数","必要単位数","不足単位数"]

    result=[data,label,dfdata,dflabel,score_data,score_label,dfscore_data,dfscore_label]
    return result
"""
    if passcheck==401:
        data,label,dfdata,dflabel,score_data,score_label,dfscore_data,dfscore_label=[1,1,1,1,1,1,1,1]
        result=[data,label,dfdata,dflabel,score_data,score_label,dfscore_data,dfscore_label]
        return result
    else:
        pass
"""

# 円グラフの描画関数
def show_piegraph(rsl):
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    from matplotlib.font_manager import FontProperties

    import numpy as np
    import pandas as pd

    plt.style.use('ggplot')
    plt.rcParams.update({'font.size':15})

    ###各種パラメータ###
    size=(9,5) #凡例を配置する関係でsizeは横長に
    col=cm.Spectral(np.arange(len(rsl[0])+5)/float(len(rsl[0])+5)) #color指定はcolormapから好みのものを。

    ###pie###
    plt.figure(figsize=size,dpi=100)
    plt.pie(rsl[0],colors=col,counterclock=False,startangle=90,autopct=lambda p:'{:.1f}%'.format(p) if p>=5 else '')
    plt.subplots_adjust(left=0,right=0.7)
    plt.legend(rsl[1],fancybox=True,loc='center left',bbox_to_anchor=(0.9,0.5))
    plt.axis('equal')
    plt.savefig('figure.png',bbox_inches='tight',pad_inches=0.05)
    plt.show()

    df1=pd.DataFrame({"スコア":rsl[3],"授業数":rsl[2]})
    #display(df1.loc[:,("スコア","授業数")])

    plt.style.use('ggplot')
    plt.rcParams.update({'font.size':15})

    ###各種パラメータ###
    size=(9,5) #凡例を配置する関係でsizeは横長に
    col=cm.Spectral(np.arange(len(rsl[4]))/float(len(rsl[4]))) #color指定はcolormapから好みのものを。
    c_cycle=(
             "#446cb3","#d24d57","#27ae60","#663399","#f7ca18","#bdc3c7","#2c3e50","#d35400",
             "#9b59b6","#ecf0f1","#ecef57","#9a9a00","#8a6b0e",
            "#1498db","#51a62d","#1abc9c","#9b59b6","#f1c40f","#7f8c8d","#34495e")

    ###pie###
    plt.figure(figsize=size,dpi=100)
    plt.pie(rsl[4],colors=col,counterclock=False,startangle=90,autopct=lambda p:'{:.1f}%'.format(p) if p>=5 else '')
    plt.subplots_adjust(left=0,right=0.7)
    plt.legend(rsl[5],fancybox=True,loc='center left',bbox_to_anchor=(0.9,0.5))
    plt.axis('equal')
    plt.savefig('figure.png',bbox_inches='tight',pad_inches=0.05)
    plt.show()

    df1=pd.DataFrame({"スコア":rsl[7],"単位数":rsl[6]})
    #display(df1.loc[:,("スコア","単位数")])

# 取得単位数や達成率のデータセットを整形する関数
def bargraph_dataset(tables):
    import pandas as pd
    import numpy as np

    df_rm=tables[2]
    main_unit=tables[4]

    df_rm2=df_rm.set_index("区分名")
    rm101=df_rm2[['必要単位数', '修得単位数']]
    rm102=df_rm2[['履修単位数',"不足単位数"]]
    rm103=df_rm2[["現在達成率(%)","予定達成率(%)"]]

    cl1= ['区分名', '必要単位数', '修得単位数', '履修単位数', '不足単位数', '備考']
    cl2=[rm101,rm102,rm103]

    result=[rm101,rm102,rm103]

    return result

# 棒グラフ等の描画関数
def show_bargraph(rsl):
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    from matplotlib.font_manager import FontProperties
    plt.style.use('ggplot')

    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\msgothic.ttc', size=14)

    rsl[0].plot.bar(color=['#348ABD', '#7A68A6', '#A60628'],figsize=(12,3))
    plt.xticks( fontproperties=fp)  #x軸
    plt.legend(loc="upper left", prop=fp)
    #display(rsl[0])

    rsl[1].plot.bar(color=['#348ABD', '#7A68A6', '#A60628'],figsize=(12,3))
    plt.xticks( fontproperties=fp)  #x軸
    plt.legend(loc="upper left", prop=fp)
    #display(rsl[1])

    rsl[2].plot.bar(color=['#348ABD', '#7A68A6', '#A60628'],figsize=(12,3))
    plt.xticks( fontproperties=fp)  #x軸
    plt.legend(loc="lower left", prop=fp)
    #display(rsl[2])
