from pycord.base3_106 import func1
from pycord.base3_106 import speed_optimisation1
from pycord.myGraphstock_101 import piegraph_dataset
from pycord.myGraphstock_101 import bargraph_dataset
from pycord.dataset_for_database import dataset_for_database
from pycord.dataset_for_database import personal_dataset_for_database
def condact(value):
    uservalue=value
    if uservalue[0]=='lilith':
        uservalue[0]='16bc046c'
        uservalue[1]='emCHwBWs'
        first = 0
    elif uservalue[0]=='first_to_fast':
        first = 1
    else:
        first = 0
    #from pycord.base3_106 import func1

    try:
        if first == 1:
            result,kyoushoku_c,passcheck = speed_optimisation1()
                        
        else:
            result,kyoushoku_c,passcheck=func1(uservalue)
        if passcheck==1:
            pass
        elif passcheck==401:
            pass

        elif passcheck==11:
            result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck=[1,1,1,1,1,1,11]        
            return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck
        elif passcheck==12:
            result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck=[1,1,1,1,1,1,12]        
            return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck

        else:
            result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck=[1,1,1,1,1,1,0]        
            return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck

    except Exception as e:
        result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck=[1,1,1,1,1,1,2]        
        return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck        

    try:
        #from pycord.myGraphstock_101 import piegraph_dataset
        dataset_pie=piegraph_dataset(result,passcheck)
        #from myGraphstock_101 import show_piegraph
        #show_piegraph(dataset_pie)
    
    except Exception as e:
        result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck=[1,1,1,1,1,1,3]        
        return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck        
    
    try:
        #from pycord.myGraphstock_101 import bargraph_dataset
        dataset_bar=bargraph_dataset(result)
        #from myGraphstock_101 import show_bargraph
        #show_bargraph(dataset_bar)
    except Exception as e:
        result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck=[1,1,1,1,1,1,3]        
        return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck        
    
    try:


        #from pycord.dataset_for_database import dataset_for_database
        database_dataset=dataset_for_database(result,uservalue,passcheck)
        # DBのテーブルは既に作成済みとする
        #from dataset_for_database import newdata_judgement
        #newdata_judgement(database_dataset,uservalue)

    except Exception as e:
        result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck=[1,1,1,1,1,1,4]        
        return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck        

    try:
        #from pycord.dataset_for_database import personal_dataset_for_database
        personal_dataset=personal_dataset_for_database(result,uservalue)

    except Exception as e:
        result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck=[1,1,1,1,1,1,5]        
        return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck        

    if passcheck==401:
        passcheck=1
    else:
        pass
    #table=[database_dataset,personal_dataset]
    return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c, passcheck
