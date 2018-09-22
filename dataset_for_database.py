
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
    
    # 09/14
    c=table.query('unit!="NaN"')[["unit"]].astype(int)
    c.columns=["unit_int"]
    table=pd.concat([table,c],axis=1)

    c=table.query('year!="NaN"')[["year"]].astype(int)
    c.columns=["year_int"]
    table=pd.concat([table,c],axis=1)

    c=table[["grade_score"]].replace("NaN",0)
    #c=table.query('grade_score!="NaN"')[["grade_score"]].astype(int)
    c.astype(int)
    c.columns=["grade_score_int"]
    table=pd.concat([table,c],axis=1)

    c=table[["result_score"]].replace("NaN",0)
    #c=table.query('result_score!="NaN"')[["result_score"]].astype(int)
    c.astype(int)
    c.columns=["result_score_int"]
    table=pd.concat([table,c],axis=1)

    c=table[["gpa_data"]].replace("NaN",0)
    # c=table.query('gpa_data!="NaN"')[["gpa_data"]].astype(float)
    c.astype(float)
    c.columns=["gpa_int"]
    table=pd.concat([table,c],axis=1)

    table=table[["subjectnum","managementnum","user_id","subjectname","unit_int","grade","grade_score_int","result_score_int","year_int","season","teacher","gpa_int","category1","category2","last_login"]]
    table.columns=["subjectnum","managementnum","user_id","subjectname","unit","grade","grade_score","result_score","year","season","teacher","gpa","category1","category2","last_login"]
 
    return table

def personal_dataset_for_database(result,uservalue):
    import pandas as pd
    import numpy as np
    user_info=result[0]
    gpa_info=result[1]
    user_id=uservalue[0]
    user_id=[user_id]
    user_id=pd.DataFrame({
        "user_id":user_id
    })

    npu_info=np.array(user_info)
    student_grade=npu_info[3,0]
    student_grade=int(student_grade)
    student_grade=[student_grade]
    student_grade=pd.DataFrame({
        "student_grade":student_grade
    })
    personal_df=pd.concat([user_id,student_grade],axis=1)

    value=npu_info[2,3]
    value=int(value)
    value=[value]
    value=pd.DataFrame({
        "enteryear":value
    })
    personal_df=pd.concat([personal_df,value],axis=1)

    value=npu_info[2,4]
    value=int(value)
    value=[value]
    value=pd.DataFrame({
        "seasons":value
    })
    personal_df=pd.concat([personal_df,value],axis=1)

    gpa_np=np.array(gpa_info.query('index!=0 & index!=1')[["累計"]])
    value=gpa_np[len(gpa_np)-1,0]
    value=float(value)
    value=[value]
    value=pd.DataFrame({
        "gpa":value
    })
    personal_df=pd.concat([personal_df,value],axis=1)
    return personal_df

def newdata_judgement(database_dataset,uservalue):
    new_table=database_dataset
    USER=uservalue[0]

    import pandas as pd
    import numpy as np
    import psycopg2
    from sqlalchemy import create_engine
    connection_config={
        'host':'localhost',
        'port':'5432',
        'database':'gradedb',
        'user':'shunsuke',
        'password':'shun0210'
    }
    connection=psycopg2.connect(**connection_config)
    cur=connection.cursor()

    connection.commit()
    where_id=USER
    cur.execute("SELECT * FROM gradetable3 WHERE user_id = %s;",(where_id,))
    sql=cur.query
    inserted_table=pd.read_sql(sql,con=connection)

    new=len(new_table)
    already=len(inserted_table)
    npnew=np.array(new_table)
    npalready=np.array(inserted_table)

    if already==0:
        url='postgresql+psycopg2://shunsuke:shun0210@localhost:5432/gradedb'
        engine=create_engine(url,echo=True)
        new_table.to_sql('gradetable3',engine,index=False,if_exists='append')
        print("passed-1")

    elif new > already:

        removefirst=pd.DataFrame(npnew[0,:])
        removefirst=removefirst.T

        news=npnew[:,1]
        alrs=npalready[:,1]

        for i in range(len(news)):
            s1=news[i]
            s1c=len(news)
            for r in range(len(alrs)):
                s2=alrs[r]
                s2c=len(alrs)-1
                if s1==s2:
                    break
                elif s2c==r:
                    newrow=pd.DataFrame(npnew[i,:])
                    newrow=newrow.T
                    removefirst=pd.concat([removefirst,newrow],axis=0)
                else:
                    pass
        display(removefirst)
        removefirst=np.array(removefirst)
        removed=pd.DataFrame(removefirst[1:,:])

        url='postgresql+psycopg2://shunsuke:shun0210@localhost:5432/gradedb'
        engine=create_engine(url,echo=True)
        removed.to_sql('gradetable3',engine,index=False,if_exists='append')
        print("passed-2")
    else:
        print("passed-3")

