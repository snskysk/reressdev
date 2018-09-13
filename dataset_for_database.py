
# coding: utf-8

# In[10]:


def dataset_for_database(result,uservalue):
    import datetime
    import numpy as np
    import pandas as pd
    table=result[3]
    user=uservalue[0]
    d_today = datetime.date.today()

    user_id=[]
    last_login=[]
    for i in range(len(table)+100):
        user_id.append(user)
        last_login.append(d_today)

    user_id=np.array(user_id)
    user_id=pd.DataFrame({
        "user_id":user_id
    })
    last_login=np.array(last_login)
    last_login=pd.DataFrame({
        "last_login":last_login
    })

    table=pd.concat([table,user_id],axis=1)
    table=pd.concat([table,last_login],axis=1)
    table=table.query('unit=="1"|unit=="2"|unit=="4"|unit=="6"|unit=="8"')
    return table
