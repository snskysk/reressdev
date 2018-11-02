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

    #単位取得の達成率(ゲージ用)
    #取得単位数と必要単位数
    #get_unit, required_unit, r_unit = list_pie[6][5:]
    #params['get_unit'] = get_unit
    #params['required_unit'] = required_unit
    #params['r_unit'] = r_unit
    #gradeAchievementは全体の単位取得率
    #gradeAchievement = (get_unit / required_unit) * 100
    #params['gradeAchievement'] = gradeAchievement

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
