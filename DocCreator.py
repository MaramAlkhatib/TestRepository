
import pyodbc, json, datetime, os
import pandas as pd
import re
from docxtpl import DocxTemplate, InlineImage
from docx import Document
from colorama import Fore, Back, Style
from jinja2 import Environment, FileSystemLoader


conn=pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T')

www='4002348246-R0000009'

CityName = {
    "11":"Riyadh",
    "12":"Qassim",
    "13":"AlKharj",
    "14":"Riyadh Outer",
    "15":"Hail",
    "16":"Dawadmi",
    "31":"Dammam",
    "32":"Hasssa",
    "33":"North Area",
    "34":"AlJouf",
    "35":"North Boarder"}

EqRating = {
    '000':{'Type':'Breaker','Rating':'200A'},
    '001':{'Type':'Breaker','Rating':'300A'},
    '002':{'Type':'Breaker','Rating':'500A'},
    '003':{'Type':'Breaker','Rating':'800A'},
    '004':{'Type':'Breaker','Rating':'250A'},
    '005':{'Type':'Breaker','Rating':'400A'},
    '006':{'Type':'Breaker','Rating':'600A'},
    '007':{'Type':'Breaker','Rating':'1000A'},
    '008':{'Type':'Breaker','Rating':'160A'},
    '201':{'Type':'Meter','Rating': 'CT/CTVT'},
    '203':{'Type':'Meter','Rating': '100A'},
    '204':{'Type':'Meter','Rating': '160A'},
    '208':{'Type':'Meter','Rating':'WC100A'},
    '207':{'Type':'Meter','Rating':'WC160A'},
    '206':{'Type':'Meter','Rating':'SMCT'},
    '205':{'Type':'Meter','Rating':'SMCTVT'},
    '302':{'Type':'DCU','Rating':'DCU'},
    '209':{'Type':'Communication Module','Rating': '100A'}
    
}

MeterTypes = {
                'AEC':'AECL',
                'DZG':'Universal Project Company UPC',
                'ECC':'ENERGYCARE',
                'GRT':'GLOBALTRONICS',
                'HLY':'HOLLEY',
                'KFM':'KAIFA',
                'LYE':'LINYANG',
                'MMF':'MEMF',
                'SXE':'SANXING',
                'SMR':'Saudi Meter Company SMC',
                'AES':'ZIV-Alfanar',
                'REC':'LOWAN',
                'AED':'AED-Alfanar',
                'CHT':'CHT-Alfanar',
                'MMF':'MEMF'
            }


CommunicationType = {
    'KFM2020860':{'Type':'NB-IoT'},
    'KFM2120860':{'Type':'NB-IoT'},
    'KFM2020760':{'Type':'NB-IoT'},
    'KFM2120760':{'Type':'NB-IoT'},
    'KFM2020766':{'Type':'PLC'},
    'KFM2120766':{'Type':'PLC'},
    'KFM2020660':{'Type':'NB-IoT'},
    'KFM2120660':{'Type':'NB-IoT'},
    'KFM2020560':{'Type':'NB-IoT'},
    'KFM2120560':{'Type':'NB-IoT'},
    'KFM2030298':{'Type':''},
    'KFM2020695':{'Type':''},
    'DZG':{'Type':'NB-IoT'},
    'AEC':{'Type':'NB-IoT'},
    'SXE':{'Type':'NB-IoT'},
    'LYE':{'Type':'NB-IoT'},
    'ECC':{'Type':'NB-IoT'},
    'MMF2020800':{'Type':'NB-IoT'},
    'AES':{'Type':'PLC'},
    'SMR2020850':{'Type':'NB-IoT'},
    'SMR2020856':{'Type':'PLC'},
    'REC':{'Type':'Communication Module'},
    'AED':{'Type':''},
    'MMF2000':{'Type':''},
    'MMF2100':{'Type':''} 
}

################################################################################################################################################################################
################################################################################################################################################################################
##################################################################### PDF Doc ##################################################################################################

def DocumentCreator(NCRNumber):
    # NCRNumber = '4009181608-R0000001'
    print(NCRNumber)
    print(Fore.BLUE +"Creating Doc for "+str(NCRNumber) +Style.RESET_ALL)
    print("Create Doc for"+str(NCRNumber))
    
    SQLStr = """
                select  SAI.NCRNumber, 
                		sai.MainNCRNumber, 
                		format(SAI.CreationDateTime,'yyyy-MM-dd HH:mm:ss') as CreationDateTime, 
                		concat(UAC.FirstName , ' ' , UAC.LastName) as CreatedBy,
                		format(SAI.CloseDate,'yyyy-MM-dd HH:mm:ss') as CloseDate,
                		concat(UACl.FirstName , ' ' , UACl.LastName) as ClosedBy,
                		SAI.Resposability,
                		format(FinalCompletionDatetime, 'yyyy-MM-dd HH:mm:ss') as FinalCompletionDatetime,
                		RectifiedBy,
                		NCRFullData,
                		OrderData,
                		OESerial, OERating,
                		NESerial,NERating,
                		NCT.[Type],
                        sai.Premise,
                        SAI.HostOrderNumber,
		                Reas.Reason,
		                Reas.SubReason,
                        SAI.Invest,
						Sts.Status,
                        SAI.LastComment,
                          (SELECT
                            COUNT(id)
                        FROM
                            SAI_NCRs
                        WHERE
                            MainNCRNumber='"""+ NCRNumber +"""') as 'SubNum'

                from 
                	SAI_NCRs SAI
                	inner join Clevest.dbo.WorkOrder WOM on WOM.HostOrderNumber=SAI.HostOrderNumber
                	inner join SAI_UserAccount UAC on UAC.id = SAI.CreatedBy
                    inner join SAI_BM_Reasons Reas on Reas.id = SAI.NCRReasonID
					left join SAI_NCR_Statuses Sts on Sts.id = EStatus
                	left join SAI_UserAccount UACl on UACl.id = SAI.ClosedBy
                	left join SAI_NCRTypes NCT on NCT.id = SAI.NCRType
                where 
                    NCRNumber='"""+ NCRNumber +"""' or MainNCRNumber='"""+ NCRNumber +"""'"""
    
    NCRAllData = pd.read_sql(SQLStr, conn)
    print(NCRAllData)
    NCRAllData = NCRAllData.fillna("NA")
    MainNCR = NCRAllData[NCRAllData["Type"].isin(["Main"])]
    SUBNCRs = NCRAllData[~NCRAllData["MainNCRNumber"].isin(["NA"])]
    
    OrderData = json.loads(MainNCR.iloc[0]["NCRFullData"])
    ClevestData = json.loads(MainNCR.iloc[0]["OrderData"])
    Office = OrderData["Office"]
    Region = ('COA' if Office[:1]=='1' else 'EOA') + ' - ' + CityName[Office[:2]]
    RepDate = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print("Retrived Data: "+str(NCRAllData))
    print("--------------------")
    print("MainNCR Data: "+str(MainNCR))
    # print(NCRAllData["SubNum"][0])
    
    MainContext = {
                    "Region" : Region,
                    "Office" : Office,
                    "Premise" : OrderData["Premise"],
                    "CrBy" : OrderData["RaisedBy"],
                    "WNO" : MainNCR.iloc[0]["RectifiedBy"]
                    ,"RevBy" : MainNCR.iloc[0]["ClosedBy"]
                    ,"Resp" : MainNCR.iloc[0]["Resposability"]
                    ,"CrDate" : MainNCR.iloc[0]["CreationDateTime"]
                    ,"RecDate" : MainNCR.iloc[0]["FinalCompletionDatetime"]
                    ,"CloseDate" :MainNCR.iloc[0]["CloseDate"] 
                    ,"SS" : OrderData["Subscription"]
                    ,"HON" :MainNCR.iloc[0]["HostOrderNumber"] 
                    ,"RefNum" : MainNCR.iloc[0]["NCRNumber"]
                    ,"Reason" : MainNCR.iloc[0]["Reason"], "SubReason":MainNCR.iloc[0]["SubReason"]
                    ,"Inves" : MainNCR.iloc[0]["Invest"]
                    ,"DocDate" : RepDate
    
                }
    Context = {
                    "Region" : Region,
                    "Office" : Office,
                    "Premise" : OrderData["Premise"],
                    "CrBy" : OrderData["RaisedBy"],
                    "WNO" : MainNCR.iloc[0]["RectifiedBy"]
                    ,"RevBy" : MainNCR.iloc[0]["ClosedBy"]
                    ,"Resp" : MainNCR.iloc[0]["Resposability"]
                    ,"CrDate" : MainNCR.iloc[0]["CreationDateTime"]
                    ,"RecDate" : MainNCR.iloc[0]["FinalCompletionDatetime"]
                    ,"CloseDate" :MainNCR.iloc[0]["CloseDate"] 
                    ,"SS" : OrderData["Subscription"]
                    ,"HON" :MainNCR.iloc[0]["HostOrderNumber"] 
                    ,"RefNum" : MainNCR.iloc[0]["NCRNumber"]
                    ,"Reason" : MainNCR.iloc[0]["Reason"], "SubReason":MainNCR.iloc[0]["SubReason"]
                    ,"Inves" : MainNCR.iloc[0]["Invest"]
                    ,"DocDate" : RepDate
    
                }
    
    NEques = []
    OEques = []
    NECnt = 1
    OECnt = 1

    #print(SUBNCRs)
    for i, row in SUBNCRs.iterrows():
        print(i)
        print(row)
        print('______________________')
        if row["NESerial"]=='NA':
            pass
        else:
            NEques.append({"s":str(NECnt) , "Type":row["Type"] , "SN":row["NESerial"], "Man":MeterTypes[row["NESerial"][:3]], "CMNT":'' if row["LastComment"]=='NA' else row["LastComment"], "st":""})
            NECnt += 1
        if row["OESerial"]=='NA':
            pass
        else:
            OEques.append({"s":str(OECnt) , "Type":row["Type"] , "SN":row["OESerial"], "Man":MeterTypes[row["OESerial"][:3]], "CMNT":'' if row["LastComment"]=='NA' else row["LastComment"], "st":row["Status"]})
            OECnt += 1
            DEqs = {"Eqs":OEques}
            EEqs = {"Eqs":NEques}
            if row["OESerial"][0:10] in CommunicationType:

                commTech= CommunicationType[row["OESerial"][0:10]]["Type"]

            elif row["OESerial"][0:3] in CommunicationType:

                commTech= CommunicationType[row["OESerial"][0:3]]["Type"]

            else:

                commTech= ''

            Inves = re.sub(r'[^a-zA-Z0-9 \.]','',MainNCR.iloc[0]["Invest"])
            EqContext = {
             
                    "ReportName":"SubNCR\n",
                    "OutputFile":"D:\\SAI_System\\templates\\NCRs\\"+NCRNumber+"\\"+ row["NCRNumber"]+".pdf"+"\n"
                    ,"Region" :Region+"\n"
                    ,"Office" : Office+"\n"
                    ,"Premise":OrderData["Premise"]+"\n"
                    ,"CrBy" : OrderData["RaisedBy"]+"\n"
                    ,"WNO" : MainNCR.iloc[0]["RectifiedBy"]+"\n"
                    ,"RevBy" : MainNCR.iloc[0]["ClosedBy"]+"\n"
                    ,"Resp" : MainNCR.iloc[0]["Resposability"]+"\n"
                    ,"CrDate" :MainNCR.iloc[0]["CreationDateTime"]+"\n"
                    ,"RecDate" : '' if MainNCR.iloc[0]["FinalCompletionDatetime"]=='NA' else MainNCR.iloc[0]["FinalCompletionDatetime"]+"\n"
                    ,"NoEq" : str(NCRAllData["SubNum"][0])+"\n"
                    ,"CloseDate" : '' if MainNCR.iloc[0]["CloseDate"]=='NA' else MainNCR.iloc[0]["CloseDate"]+"\n"
                    ,"SS" :OrderData["Subscription"]+"\n"
                    ,"HON" :MainNCR.iloc[0]["HostOrderNumber"]+"\n"
                    ,"RefNum" : MainNCR.iloc[0]["NCRNumber"]+"\n"
                    ,"Reason" : MainNCR.iloc[0]["Reason"], "SubReason":MainNCR.iloc[0]["SubReason"]+"\n"
                    ,"Inves" : Inves+"\n"
                    ,"DocDate" : RepDate+"\n"
                    ,"EqSN" : row["OESerial"]+"\n"
                    ,"Rating" : EqRating[row["OESerial"][5:8]]["Rating"]+"\n" 
                    ,"CommType" :commTech+"\n"
                    ,'EqType' : EqRating[row["OESerial"][5:8]]["Type"]+"\n"
                    ,"DEqs" : DEqs
                    ,"EEqs" : EEqs
                }
    # ---------Main---------
    DEqs = [{"Eqs":OEques}]
    EEqs = [{"Eqs":NEques}]
    MainContext["DEqs"] = DEqs
    MainContext["NEqs"] = EEqs
    doc = DocxTemplate("templates/NCRs/Templates/NCRMain1.docx")
    try:
        os.mkdir("templates/NCRs/" + NCRNumber)
    except:
        pass
    doc.render(EqContext)
    set_of_variables = doc.get_undeclared_template_variables()
    print(set_of_variables)
    doc.save("templates/NCRs/" + NCRNumber + "/"+ NCRNumber +".docx")
    print(Fore.GREEN +"Doc Created for "+str(NCRNumber) +Style.RESET_ALL)
    print(EqContext)
    print(row["NCRNumber"])
    # print(EqContext)

    # ---------SUB---------
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('DocCreator.html')
    output_from_parsed_template = template.render(EqContext)
    print(output_from_parsed_template)

    # to save the results
    with open(r"D:\\SAI_System\\templates\\ReportMonitoringFolder\\"+NCRNumber+datetime.datetime.today().strftime('%Y%m%d%H%M%S')+".srpt", "w") as fh:
        fh.write(output_from_parsed_template)


# DocumentCreator('4008003392-R0000001')