def pytojsMaterials(result, list_pie, list_bar, table):
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

    #単位取得の達成率(ゲージ用)
    #取得単位数と必要単位数
    get_unit, required_unit = list_pie[6][5:7]
    #gradeAchievementは全体の単位取得率
    gradeAchievement = (get_unit / required_unit) * 100
    params['gradeAchievement'] = gradeAchievement

    #単位の取得率(ex:専門選択の取得パーセンテージ)
    Achivement_list = list(list_bar[2]['現在達成率(%)'])
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


    return params
