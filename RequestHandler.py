import warnings

warnings.filterwarnings('ignore')
import pandas as pd
import time,os
from pandas.io import sql
import DocCreator as GenDoc
import pyodbc, json, uuid
ClConnectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=HO-MWFMDB.alfanar.com,1433;DATABASE=Clevest;UID=clevest;PWD=!C13ve$T'
clConn = pyodbc.connect(ClConnectionStr)
cr = clConn.cursor()
RequestSatus = pd.read_sql("Select * FROM [HES].[dbo].[SAI_NCR_Request_Status]", clConn)

def RequestQueue(Req):
    print(Req)
    InsertStr = """ Insert INTO [HES].[dbo].[SAI_NCR_Request_Queue]
                                ([HostOrderNumber],[Insert_Date],[Request_Status],[Source_Data],[Clevest_Msg],[RequestedBy])
                        VALUES"""
    for k in Req.keys():
        inProcess = Req[k]
        
        HostOrderNumber = inProcess["PNum"]
        UId = inProcess["UId"]
        InsertData = """('"""+ HostOrderNumber +"""',getdate(),1,'"""+ json.dumps(Req).replace("'", '"')  +"""',Null,"""+ str(UId) +""")"""
    global clConn
    print(InsertStr + " " + InsertData )
    cr.execute(InsertStr + " " + InsertData )
    print("-----------Request Added------")
    clConn.commit()