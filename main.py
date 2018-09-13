def condact(value):
    uservalue=value
    from base3_106 import func1
    result=func1(uservalue)

    from myGraphstock_101 import piegraph_dataset
    dataset_pie=piegraph_dataset(result)
    #rom myGraphstock_101 import show_piegraph
    #show_piegraph(dataset_pie)

    from myGraphstock_101 import bargraph_dataset
    dataset_bar=bargraph_dataset(result)
    #from myGraphstock_101 import show_bargraph
    #show_bargraph(dataset_bar)

    from dataset_for_database import dataset_for_database
    database_dataset=dataset_for_database(result,uservalue)

    #return database_dataset
    return result, dataset_pie, dataset_bar, database_dataset
