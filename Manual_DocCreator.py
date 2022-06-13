def testfunc(prem):
    print(prem)

# documents=pd.read_sql("""SELECT TOP(10) 
#                             nc.NCRNumber ,
#                             ST.Status as StatusName,
#                             nc.Status as StatusNum
#                             FROM 
#                             [HES].[dbo].[SAI_NCRs] as nc      
#                             LEFT JOIN HES.dbo.SAI_NCR_Statuses as ST ON ST.id = nc.Status                          
                         
#                             """,clConn)
# documents.to_csv("testing data.csv")
documents = pd.read_csv("testing data.csv")

import os
import numpy as np
# import DocCreator as DocGen

documents["SubNCRNumber"] = documents[documents['StatusNum']==7]['NCRNumber']
documents["SubNCRNumber"] = documents["SubNCRNumber"].fillna("")
# documents["NCRNumber"]=documents[~documents["NCRNumber"].str.contains("_")]
# documents["NCRNumber"] = documents[documents['StatusNum']!=1014]['NCRNumber']

path = r"C:\\Users\\Maram.Alkhatib\\OneDrive - alfanar\\Documents\\SMP2022\\templates\\NCRs\\"
for i in documents["NCRNumber"]:
        if "_" not in i:
            path1= path + i 
            # print(i)
            if os.path.exists(path1):
                pass
            else:
                # pass
                # os.mkdir(path1)
                print("Directory '%s' created" %i)

for i in documents["SubNCRNumber"]:
        if i != "":
            # print(i)
            main = i.split("_")[0]
            path1= path + main +"\\"+ i
            # print(path1)
            if os.path.exists(path1):
                pass
            else:
                # pass
                # print(path1)
                # DocGen(main)
                print("Directory '%s' created" %i)
