
def condact(value):
    uservalue=value
    if uservalue[0]=='lilith':
        uservalue[0]='16bc046c'
        uservalue[1]='emCHwBWs'
    else:
        pass
    from pycord.base3_106 import func1
    result,kyoushoku_c=func1(uservalue)

    from pycord.myGraphstock_101 import piegraph_dataset
    dataset_pie=piegraph_dataset(result)
    #from myGraphstock_101 import show_piegraph
    #show_piegraph(dataset_pie)

    from pycord.myGraphstock_101 import bargraph_dataset
    dataset_bar=bargraph_dataset(result)
    #from myGraphstock_101 import show_bargraph
    #show_bargraph(dataset_bar)

    from pycord.dataset_for_database import dataset_for_database
    database_dataset=dataset_for_database(result,uservalue)
    # DBのテーブルは既に作成済みとする
    #from dataset_for_database import newdata_judgement
    #newdata_judgement(database_dataset,uservalue)

    from pycord.dataset_for_database import personal_dataset_for_database
    personal_dataset=personal_dataset_for_database(result,uservalue)

    #table=[database_dataset,personal_dataset]
    return result, dataset_pie, dataset_bar, database_dataset, personal_dataset, kyoushoku_c
