#from crypt import methods
#from crypt import methods
from asyncio.windows_events import NULL
import csv
from itertools import groupby
import re
from bs4 import BeautifulSoup
from opcode import opname
import GetOrderPhotos as GOP
import os, random, math, smtplib, ssl, json,  time, glob
from posixpath import split
from flask import Flask, request,  render_template, redirect, make_response, send_from_directory,abort, send_file,Response
from pandas.core.frame import DataFrame
from pandas.io import excel
import requests
from requests.auth import HTTPBasicAuth
from pandas.io.sas import sasreader
from werkzeug.utils import secure_filename
from datetime import datetime
from datetime import timedelta
from subprocess import Popen
from win32process import DETACHED_PROCESS, THREAD_PRIORITY_TIME_CRITICAL
import pyodbc
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import socket
from werkzeug.utils import secure_filename
from colorama import Fore, Back, Style
from threading import Thread
import shutil
#import SimManagement
import GetMeterData as GMD
import HTML_Builder as BH
import UserManagement as UM
import ECBRevision as ECR
# from MeterManuData import UploadMeterData as UMD
import globalFunctions as GFs
import EMailer as mailIt
import NCR_Management1 as NCRM
import DocCreator as GenDoc
# import logging.handlers
import logging.handlers as handlers


import MultiFilrEmailer as mailer
import logging
from PlanManagement.PM import PM as PlanManage

import warnings
warnings.filterwarnings('ignore')
PlanEndTime = 19

# from termcolor import colored, cprint
DownloadFilesFolder = "D:\\SAI_System\\"

key = b'JNQcis_GHIF_-kQUkCbJV4VsShKpnPvf-4zSrSysT-Q='
SystemToken = "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiJiMTIwZjE2Mi1lN2VjLTQwZDctYjgxOC0wOGQ4ZjM3Yzg1MGMiLCJ1bmlxdWVfbmFtZSI6IntcIklkXCI6XCJiMTIwZjE2Mi1lN2VjLTQwZDctYjgxOC0wOGQ4ZjM3Yzg1MGNcIixcIlVzZXJuYW1lXCI6XCJXRk1TXCIsXCJQYXNzd29yZEhhc2hcIjpcIjJtWWU1R3d6dE44dDJLQmtIL1QwWGljVnFXTE5pTk5BeVFQeFJlVzZNdENyYk1MY2NycXk1RzR1R1pxYW9qSldHV0p6OTZORXpzalNidkpXZC9aQVVBPT1cIixcIlBhc3N3b3JkU2FsdFwiOlwiY1BSSWk5SHc0eGpVamdQdTNSMWE2bTdxNkNIc0JNYzRCb0Q2R1FEVW9kNVQyNEUrWXNhMWQ3ZXk4b1JFZGFnS0p5ZFRUaGpzN2xOOEJXOFpBWTF0bVZGbkNNTjIzSWUvNXZFeHlpcmxFS3F0VWVuUmdibUNOYk9rRkVSWVZVeS9lYy9WK2E5Q2lBZzdFSUVmM2EwcHJ1eHpvQTdpb0JPUjc4Q25UTXROTkRjPVwiLFwiRmlyc3ROYW1lXCI6XCJXRk1TXCIsXCJMYXN0TmFtZVwiOlwiV0ZNU1wiLFwiRW1haWxcIjpcIldGTVNAZS1pbmN1YmUuY29tXCIsXCJTb3VyY2VDb2RlXCI6XCJXRk1TXCIsXCJTb3VyY2VOYW1lXCI6XCJXRk1TXCIsXCJJc0ZvVXNlclwiOmZhbHNlLFwiRnVsbE5hbWVcIjpcIldGTVMgV0ZNU1wifSIsInJvbGUiOiJbXSIsIm5iZiI6MTYyODUxNzkxOSwiZXhwIjoxNjI4NjA0MzE5LCJpYXQiOjE2Mjg1MTc5MTl9.W_n9Yuw3nebslBXLs96DN2SD1cHqjI3Q-E48mc7l7gS_OZd9uJwejLr3YrQwiXrJ98wUniDk5p-lQTVZ9AuO4Q"

from cryptography.fernet import Fernet
import uuid

ClConnectionStr = 'DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=Clevest;UID=clevest;PWD=!C13ve$T'

myPM = PlanManage(ClConnectionStr)

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T')

app = Flask(__name__, static_folder='templates', instance_path='D:\\SAI_System\\downloads')
app.config['UPLOAD_EXTENSIONS'] = ['.docx','.pdf']
app.config['UPLOAD_PATH'] = "templates/NCRs/"
fernet = Fernet(key)
ActiveSessions = {}
SessionDuration = timedelta(hours=48)

AssignFilesTemplates = {
    "1" : "%_Assign_MEX.csv",
    "3" : "%_Assign_ECB.csv",
    "10" : "%_Assign_BoxRep.csv",
    "5" : "%_Assign_BM.csv",
    "12" : "%_Assign_CMI.csv"
}
dict_HostExchange={
    "1" : {
            "Name" : "MEX"
            ,"FilePath" : "//10.90.10.59/prd/AllHostExchange/SingleUpdateFolder"
            ,"FileNameTemplate" : "%_Assign_MEX.csv"
          }
    ,"3" : {
            "Name" : "ECB"
            ,"FilePath" : "//10.90.10.59/prd/AllHostExchange/SingleUpdateFolder"
            ,"FileNameTemplate" : "%_Assign_ECB.csv"
          }
    ,"5" : {
            "Name" : "Smart to Smart"
            ,"FilePath" : "//10.90.10.59/prd/AllHostExchange/SingleUpdateFolder"
            ,"FileNameTemplate" : "%_Assign_BM.csv"
          }
    ,"10" : {
            "Name" : "Box Replacement"
            ,"FilePath" : "//10.90.10.59/prd/AllHostExchange/SingleUpdateFolder"
            ,"FileNameTemplate" : "%_Assign_BoxRep.csv"
          }
    ,"12" : {
            "Name" : "Comm Module Inst"
            ,"FilePath" : "//10.90.10.59/prd/AllHostExchange/SingleUpdateFolder"
            ,"FileNameTemplate" : "%_Assign_CMI.csv"
          }
}

SECMD =pd.DataFrame()

AlFanarMeters = pd.read_sql("select DeviceID as Serials from alf_meters ",conn)

AppDebugMode = True

statusList={
        "Created":"success",
        "InProgress":"warning",
        "Pending":"info",
        "Rectified":"primary",
        "Closed":"secondary"
        }

# logging.basicConfig(
#                     filename = "logfile_T.log", 
#                     filemode = "a",
#                     format = "%(asctime)s %(levelname)s - %(funcName)s - %(message)s",
#                     level = logging.DEBUG
#                     )


log_formatter = logging.Formatter('%(asctime)s %(levelname)s - %(funcName)s - %(message)s')
logFile = 'log/logfile_T.log'
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)
logHandler = handlers.RotatingFileHandler(logFile, maxBytes=10*1024*1024, backupCount=10)
logHandler.setLevel(logging.DEBUG)
logHandler.setFormatter(log_formatter)
logger.addHandler(logHandler)
console  = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console)

def IsinByPassList(Pnum):
    print("ByPass Premise: "+Pnum)
    logger.warning("ByPass Premise: "+Pnum)

    SQL=""" select  DISTINCT Premise
                from
                HES.dbo.SAI_NCR_MeterByPass
                where
                ValidTo > format(getdate(),'yyyy-MM-dd') and Premise = """+Pnum+ """
            """
    ByPass= pd.read_sql(SQL, conn)
  
    
    if len(ByPass)>0:
        
        return True
    return False




# IsinByPassList('4000621076')
def IsAlFanarMeter(SN):
    if len(AlFanarMeters[AlFanarMeters["Serials"]==SN])>0:
        return True
    return False

def ReloadSECData():
    # DCU Data
    df = pd.read_sql("""
                        SELECT    
                            wo.HostOrderNumber as Premise,
                            FORMAT(wom.FH_OfficeCode,'0000') as Office,
                            wom.FH_RouteReadSequence as 'Route Read Seq',
                            wom.FH_ServiceClass as 'Service Class',
                            wom.FH_SubscriptionNumber as 'Subscription No',
                            wom.FH_ContractAccount as 'Account No',
                            STR(wo.Latitude, 25, 5) as Latitude,
                            STR(JSON_VALUE(OrderData, '$.Order.DCU_CapturedLatitude') , 25, 5) as Longitude,
                            JSON_VALUE(OrderData, '$.Order.MEX_MRUNumber') as MRU,
                            JSON_VALUE(OrderData, '$.Order.DCU_NewSerialNumber') as 'DCUSerialNumber',
                            JSON_VALUE(OrderData, '$.Order.MEX_ExistingMeterNumber') as 'MeterList',
                            JSON_VALUE(OrderData, '$.Order.DCU_SignalStrength') as 'SignalStrength',
                            JSON_VALUE(OrderData, '$.Order.TMUCTSerialNumber') as 'fg. Ser. No',
                            JSON_VALUE(OrderData, '$.Order.TransformerID') as 'TransformerID',
                            JSON_VALUE(OrderData, '$.Order.TransformerRating') as 'TransformerRating',
                            REPLACE(REPLACE(JSON_VALUE(OrderData, '$.Order.PowerConnected'), 'Y', 'Yes'),'N','No') as 'PowerConnected',
                            JSON_VALUE(OrderData, '$.Order.PowerConnectionDate') as 'PowerConnectionDate',
                            JSON_VALUE(OrderData, '$.Order.PowerStatusUpdatedBy') as 'PowerStatusUpdatedBy',
                            REPLACE(REPLACE(JSON_VALUE(OrderData, '$.Order.CTavailable'), 'Y', 'Yes'),'N','No') as 'CTavailable',
                            REPLACE(REPLACE(JSON_VALUE(OrderData, '$.Order.CTConnected'), 'Y', 'Yes'),'N','No') as 'CTConnected',
                            JSON_VALUE(OrderData, '$.Order.CTRatio') as 'CTRatio'
                        FROM
                            Clevest.dbo.WorkOrder as wo
                            inner join Clevest.dbo.WorkOrderMapping as wom on wo.HostOrderNumber = wom.HostOrderNumber
                        WHERE
                            wo.OrderTypeId = 4 
                            and wo.OrderStatusId in (100)
                            and wom.OrderStatusId in (100)
                        """,conn)
    df["Meter Type"]= "DCU"
    df["Conn. Type"]= "4G"

    # SEC Data
    global SECMD 
    SECfiles = glob.glob( "SECMasterData/*.txt")
    li=[]
    i=0
    for filename in SECfiles:
            dfx = pd.read_csv(filename,delimiter=';',header=None, dtype=str,encoding = "utf-8",quoting=csv.QUOTE_NONE)
            i+=1
            li.append(dfx)
            print ('\r |' + ('#' * i) + ('-' * (len(SECfiles) - i)) + '| File loaded -- > ' + filename , end='')
            # logger.debug('\r |' + ('#' * i) + ('-' * (len(SECfiles) - i)) + '| File loaded -- > ' + filename )
            if AppDebugMode:
                break
    print ('\r |' + ('#' * i) + ('-' * (len(SECfiles) - i)) + '| All files loaded')
    logger.info('\r |' + ('#' * i) + ('-' * (len(SECfiles) - i)) + '| All files loaded')
    SECMD =  pd.concat(li, axis=0, ignore_index=True)
    cols=['Premise','MRU','Office','fg. Ser. No','Meter Type','Equip. No','Cycle','Last Bill Key','Route Read Seq','MR Note','Date of MR Note','Critical Need','Service Class','Premise Address','City','District','Subscription No','Account No','BPName','BP Type','Latitude','Longitude','Mult. Factor','No. of Dials','Breaker Cap.','Voltage','Phase','Tariff Type','Prev Read Date T','Prev. Read T','Prev Read Date T1','Prev. Read T1','Prev. Read Date T2','Prev. Read T2','Prev Read Date T3','Prev. Read T3','Prev. Read Date T4','Prev. Read T4','Prev. Read Date T5','Prev. Read  T5','Prev. Read Date T6','Prev. Read  T6','Prev. Read Date T7','Prev. Read  T7','Avg. Consp. per day (kWh)','Accl. Premise No','Main Premise No','Conn. Type', 'F1','F2']
    SECMD.columns=cols
    SECMD = pd.concat([SECMD, df], ignore_index=True)
    SECMD = SECMD.fillna('')
    SECMD['fg. Ser. No']= SECMD['fg. Ser. No'].str.upper()
    GMD.SECMDHere = SECMD


# ReloadSECData()

def TestAndExtendSession(SID):
    global ActiveSessions
    global SessionDuration
    
    if SID in ActiveSessions:
        CSession = ActiveSessions[SID]
        TT = datetime.strptime(CSession["ExpriationDate"], '%Y-%m-%d %H:%M:%S')
        if TT > datetime.today():
            EDate = TT + SessionDuration
            ActiveSessions[SID]["ExpriationDate"] = EDate.strftime("%Y-%m-%d %H:%M:%S")
            return True
        else:
            return False
    else:
        return False
    

def CheckUserAuth(SID, AuthCode):
    UAuths = ActiveSessions[SID]["Auths"]
    #print(UAuths)
    return True if AuthCode in UAuths else False

BM2BM_Reasons = {}

def RefreshSM2SMReasons():  
    global BM2BM_Reasons
    conn2 = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T')
    SQL = "SELECT [id],[Reason],[SubReason] FROM [HES].[dbo].[SAI_BM_Reasons] order by [Reason],[SubReason]"
    subReasons = pd.read_sql(SQL, conn2)
    conn2.close()
    bm2bm = {}
    for i, row in subReasons.iterrows():
        if row["Reason"] in bm2bm.keys():
            pass
        else:
            bm2bm[row["Reason"]] = []
        bm2bm[row["Reason"]].append([row["SubReason"],row["id"]])
    BM2BM_Reasons = bm2bm

RefreshSM2SMReasons()


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")



def USerLogIn(UName, UPass):
    global key
    global SessionDuration
    global ActiveSessions
    SQL="Select * from HES.dbo.SAI_UserAccount where UserName='" + UName + "'"
    #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T')
    UData = pd.read_sql(SQL, conn)
    if len(UData)>0:
        dbPass = UData.iloc[0].Password
        encPass = dbPass.encode()
        DBPure = fernet.decrypt(encPass).decode()
        UData = UData.fillna("")
        if DBPure==UPass:
            APPs = pd.read_sql("Select Apps.AppName, Apps.AppRout, Apps.AppDisc, Apps.AppIcon from HES.dbo.SAI_UserAppAssociation UAA inner join HES.dbo.SAI_Applications APPs on APPs.id = UAA.ApplicationId where UAA.Userid='" + str(UData.iloc[0].id) + "'  order by Apps.AppName",conn)
            Areas = pd.read_sql("Select Area from HES.dbo.SAI_UserAreaAssociation where UserId='" + str(UData.iloc[0].id) + "' order by Area",conn)
            Auths = pd.read_sql("select AuthCode from HES.dbo.SAI_Auths where id in (select authid from hes.dbo.SAI_UserAuths where userid = " + str(UData.iloc[0].id) + ")",conn)
            EAreas = pd.read_sql("Select Area from HES.dbo.SAI_UserEditAreasAssociation where UserId='" + str(UData.iloc[0].id) + "' order by Area",conn)
            EDate = datetime.today() + SessionDuration
            CSID = str(uuid.uuid1())
            print('User Name:-->"'+ UName +'"     SessionId:'+ CSID)
            logger.info('User Name:-->"'+ UName +'"     SessionId:'+ CSID)

            UApps = []
            for index, row in APPs.iterrows():
                UApps.append({"AppName":row.AppName, "AppRout": row.AppRout, "AppDisc": row.AppDisc, "AppIcon":row.AppIcon})
            UAreas=[]
            for index , row in Areas.iterrows():
                UAreas.append(row.Area)
            UEAreas=[]
            for index , row in EAreas.iterrows():
                UEAreas.append(str(row.Area))
            UAuths = []
            for index , row in Auths.iterrows():
                UAuths.append(row.AuthCode)    
            UserSessionData = {
                                "UserName":UName,
                                "UserFName":UData.iloc[0].FirstName + ' ' + UData.iloc[0].LastName,
                                "UserId":str(UData.iloc[0].id),
                                "Mail" : UData.iloc[0].Mail,
                                "Apps":UApps,
                                "Areas":UAreas,
                                "EAreas" : UEAreas,
                                "Auths":UAuths,
                                "ExpriationDate":EDate.strftime("%Y-%m-%d %H:%M:%S"),
                                "ForcePassChange" : UData.iloc[0].ForcePassChange
                               }
            ActiveSessions[CSID] = UserSessionData
            return True, CSID
        else:
            return False, ""
        
    else:
        return False, ""
    

def CheckAppInSession(SID, SRCRoute):
    global ActiveSessions
    if SID in ActiveSessions:
        for App in ActiveSessions[SID]["Apps"]:
            if App["AppRout"] == SRCRoute:
                return True
    return False

def CheckAreasInAreas(SID ,Area, Target = 'V'):
    try:
        if Area in ActiveSessions[SID]["Areas" if Target== 'E' else "EAreas"]:
            return True
        else:
            return False
    except:
        return False



def RemoveUserActiveSessions(UName):
    UserASessions=[]
    for KK in ActiveSessions.keys():
        if ActiveSessions[KK]["UserName"] == UName:
            UserASessions.append(KK)
    for LL in UserASessions:
        del ActiveSessions[LL]
    return len(LL)



def PasswordChange(UName,OldPass, NewPass):
    encNPass = fernet.encrypt(NewPass.encode()).decode()
    global key
    global SessionDuration
    global ActiveSessions
    SQL="Select * from HES.dbo.SAI_UserAccount where UserName='" + UName + "'"
    #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T')
    UData = pd.read_sql(SQL, conn)
    if len(UData)>0:
        dbPass = UData.iloc[0].Password
        encPass = dbPass.encode()
        DBPure = fernet.decrypt(encPass).decode()
        if DBPure == OldPass:
            uSQL = "update [HES].[dbo].[SAI_UserAccount] set [ForcePassChange]=0, [Password] = '"+ encNPass +"' where id=" + str(UData.iloc[0]["id"])
            k=0
            while k >= 0 and k < 10:
                k += 1
                try:
                    cr = conn.cursor()
                    cr.execute(uSQL)
                    conn.commit()
                    k = -1
                except:
                    time.sleep(.5)
            if k== -1:
                RemoveUserActiveSessions(UName)
                return {"Status" : True}
            else:
                return {"Status" : False, "Reason":"DB Connection error..."}
        else:
            return {"Status":False, "Reason":"Old Password not match."}
    else:
        return {"Status":False, "Reason":"Wrong Username"}

def ForcePassChange(UName, NewPass):
    encNPass = fernet.encrypt(NewPass.encode()).decode()
    global key
    global SessionDuration
    global ActiveSessions
    SQL="Select * from HES.dbo.SAI_UserAccount where UserName='" + UName + "'"
    #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T')
    UData = pd.read_sql(SQL, conn)
    if len(UData)>0:
        dbPass = UData.iloc[0].Password
        encPass = dbPass.encode()
        uSQL = "update [HES].[dbo].[SAI_UserAccount] set [ForcePassChange]=0, [Password] = '"+ encNPass +"' where id=" + str(UData.iloc[0]["id"])
        k=0
        while k >= 0 and k < 10:
            k += 1
            try:
                cr = conn.cursor()
                cr.execute(uSQL)
                conn.commit()
                k = -1
            except:
                time.sleep(.5)
        if k== -1:

            return {"Status" : True}
        else:
            return {"Status" : False, "Reason":"DB Connection error..."}
    else:
        return {"Status":False, "Reason":"Wrong Username"}



 
@app.route('/', methods=["GET"])    
def home():
    SID = request.cookies.get('SID')
    listSample = '''<li><a href="#ROUTE#"><div class="icon text-left"><i class='bx #FileImage#'></i></div><span>#File#</span></a></li>'''
    DWNLDList = pd.read_sql("select * from SAI_FilesDownloads where Enabled='y'",conn)
    downloads = ""
    for index, row in DWNLDList.iterrows():
        downloads += listSample.replace("#ROUTE#",'/downloads/' + row.LinkCode).replace("#FileImage#",row.FileImages).replace("#File#",row.FileName)
        # print (downloads)
    if TestAndExtendSession(SID):

        return render_template('AllApplication.html', DownloadList = downloads)
    else:
        resp = make_response(render_template('AllApplication.html', DownloadList = downloads))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp
 
    
    
#Start
@app.route('/Login', methods=["GET","POST"])
def LogIN():
    global ActiveSessions
    SID = request.cookies.get('SID')
    if request.method=="GET":
        #print(request.method)
        if TestAndExtendSession(SID):
            resp = make_response(redirect("./", code=302))
            resp.set_cookie("LoggedIn","True")
            resp.set_cookie("SID",SID)
            resp.set_cookie("UserName", ActiveSessions[SID]["UserFName"])
            return resp
        else:
            return render_template('Login.html')
    else:
        uname=request.form.get('UserName')
        upass=request.form.get('Password')
        AfterTo = request.form.get('PNext')
        Logged, SID = USerLogIn(uname, upass)
        if Logged:
            resp = make_response(redirect("./" + AfterTo, code=302))
            resp.set_cookie("LoggedIn","True")
            resp.set_cookie("SID",SID)
            resp.set_cookie("UserName", ActiveSessions[SID]["UserFName"])
            return resp
        else:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            logger.warning("Failed Login by " + str(ip_address) +" with Username: " + str(uname) + " Password: "+ str(upass))
            resp = make_response(render_template("GeneralMessage.html", MsgTitle="Login", MSGBody="Wrong Username/Password.", msgcolor = "red", BackTo="/Login"))
            resp.set_cookie("LoggedIn","False")
            resp.set_cookie("SID","")
            resp.set_cookie("ExpireDate", "")
            return resp
        
@app.route('/logout', methods=["GET"])
def LogOut():
    SID = request.cookies.get('SID')
    global ActiveSessions
    
    try:
        del ActiveSessions[SID]
    except:
        pass
    resp = make_response(redirect("./", code=302))
    resp.set_cookie("LoggedIn","False")
    resp.set_cookie("SID","")
    resp.set_cookie("ExpireDate", "")
    return resp

#Return Applications for the current user session.        
@app.route('/getapps', methods=["GET"])
def getapps():
    global ActiveSessions
    SID = request.cookies.get('SID')
    if SID in ActiveSessions:
        if TestAndExtendSession(SID):
            sss = json.dumps({"data":ActiveSessions[SID]["Apps"]})
            return json.dumps({"data":ActiveSessions[SID]["Apps"]})
        else:
            return json.dumps("{}")
    else:
        return json.dumps("{}")

@app.route('/bm', methods=["GET"])
def PrmiseData2():
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckUserAuth(SID, "MSISD"):
            return render_template('SearchMeterV2.html')
        else:
            return render_template("GeneralMessage.html", MsgTitle="Meter Search Application", MSGBody="Sorry, you don't have authority for this action.", msgcolor = "red", BackTo="../")
    else:
        resp = make_response(render_template("Login.html", NextPage = "bm"))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp    

        
@app.route('/sm', methods=["GET"])
def PrmiseData():
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckUserAuth(SID, "MSISD"):
            return render_template('SearchMeterV2.html')
        else:
            return render_template("GeneralMessage.html", MsgTitle="Meter Search Application", MSGBody="Sorry, you don't have authority for this action.", msgcolor = "red", BackTo="../")
    else:
        resp = make_response(render_template("Login.html", NextPage = "sm"))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route('/sm/showdata', methods=["POST"])
def ShowOrderData():
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        SearchKey = request.form.get('searchmethod')
        SearchData = request.form.get('SCriteria')
        SearchSRC = request.form.get('searchsource')
        print(SearchData)
        print(SearchKey)
        print(SearchSRC)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        if SearchSRC == "SEC":
            SData = GMD.GetMeterData(SearchKey, SearchData)
        else:
            SData = GMD.GetMeterDataCL(SearchKey, SearchData)
        print (SData)
        # logger.debug(str(SData)+ str(ActiveSessions[SID]["UserFName"]))

        if "data" in SData:
            print(SData['data']['Office'])
            if SData['data']['Office'] in ActiveSessions[SID]["Areas"]:
                mtype = SData['data']['MeterType']
                if mtype  == "DCU":
                    accountNum = "0"
                else:
                    accountNum =  SData['data']['AccountNumber'] 

                TTT='http://maps.google.com/maps?daddr='+ SData['data']['Latitude']+','+  SData['data']['Longitude'] +'&amp;ll='
                OpenBMHTMLStr = '''<form action="../bm/req" method="POST">
                                        <input class="w3-input w3-border" type="text" placeholder="" hidden name="PNum" id="PNum" style="font-weight: bold; text-align: center;" value="'''+ SData['data']['Premise'] +'''" readonly> </input>
                                    <div style="text-align: center;">
                                    <button type="Submit" class="btn btn-primary"  style="width: 50%"><i class='bx bxs-car-mechanic bx-tada' ></i><span> </span>Replace Meter</button>  
                                    </div>
                                    </form>'''
                ByPassMeterHTMLStr = '''<form action="../bypass/meter" method="POST">
                                      <input class="w3-input w3-border" type="text" placeholder="" required name="MNum2" hidden id="MNum2" style="font-weight: bold; text-align: center;" value="'''+ SData['data']['MeterSN'] +'''"> </input>
                                      <input class="w3-input w3-border" type="text" placeholder="" hidden name="PNum" id="PNum" style="font-weight: bold; text-align: center;" value="'''+ SData['data']['Premise'] +'''" readonly> </input>
                                    <div style="text-align: center;">
                                    <button type="Submit" class="btn btn-primary" style="width: 50%"><i class='bx bx-check-square' ></i><span> </span> Bypass Meter</button>  
                                    </div>
                                    </form>'''
                SiteVisitHTMLStr = '''<form action="../sitevisit/new" method="POST">
                                      <input class="w3-input w3-border" type="text" placeholder="" required name="MNum2" hidden id="MNum2" style="font-weight: bold; text-align: center;" value="'''+ str(SData['data']['MeterSN']) +'''"> </input>
                                      <input class="w3-input w3-border" type="text" placeholder="" required name="SS2" hidden id="SS2" style="font-weight: bold; text-align: center;" value="'''+ str(SData['data']['SubScriptionNum']) +'''"> </input>
                                      <input class="w3-input w3-border" type="text" placeholder="" required name="office2" hidden id="office2" style="font-weight: bold; text-align: center;" value="'''+ str(SData['data']['Office']) +'''"> </input>
                                      <input class="w3-input w3-border" type="text" placeholder="" required name="long2" hidden id="long2" style="font-weight: bold; text-align: center;" value="'''+ str(SData['data']['Longitude']) +'''"> </input>
                                      <input class="w3-input w3-border" type="text" placeholder="" required name="latt2" hidden id="latt2" style="font-weight: bold; text-align: center;" value="'''+ str(SData['data']['Latitude']) +'''"> </input>
                                      <input class="w3-input w3-border" type="text" placeholder="" required name="premise2" hidden id="premise2" style="font-weight: bold; text-align: center;" value="'''+ str(SData['data']['Premise']) +'''"> </input>
                                      <input class="w3-input w3-border" type="text" placeholder="" required name="mtype" hidden id="mtype" style="font-weight: bold; text-align: center;" value="'''+ str(mtype) +'''"> </input>
                                      <input class="w3-input w3-border" type="text" placeholder="" required name="acc2" hidden id="acc2" style="font-weight: bold; text-align: center;" value="'''+ str(accountNum)  +'''"> </input>
                                    <div style="text-align: center;">
                                    <button type="Submit" class="btn btn-primary" style="width: 50%"><i class='bx bxs-plane-alt' ></i><span> </span> Open Site Visit</button>  
                                    </div>
                                    </form>'''

                #Return DCU Information
                if mtype == "DCU":
                    return render_template("DCUInformationData.html",\
                                        UserName = ActiveSessions[SID]["UserFName"],\
                                        PremiseNumber=SData['data']['Premise'],\
                                        SubscriptionNumber = SData['data']['SubScriptionNum'],\
                                        AccountNumber=SData['data']['AccountNumber'], \
                                        MeterNumber = SData['data']['MeterSN'],\
                                        OfficeNumber=SData['data']['Office'],\
                                        Location=SData['data']['Latitude'] + ', ' + SData['data']['Longitude'] ,\
                                        MeterType=SData['data']['MeterType'], \
                                        MeterList=SData['data']['MeterList'],\
                                        # SignalStrength=SData['data']['SignalStrength'], \
                                        TMUNumber= SData['data']['DCUSerialNumber'], \
                                        BreakerCapacity =SData['data']['BreakerCapacity'], \
                                        MRU= SData['data']['MRU'],\
                                        EquNum= SData['data']['EquipNum'],\
                                        RSeq= SData['data']['RoutSeq'],\
                                        TransformerID= SData['data']['TransformerID'],\
                                        TransformerRating= SData['data']['TransformerRating'],\
                                        PowerConnected= SData['data']['PowerConnected'],\
                                        PowerConnectionDate= SData['data']['PowerConnectionDate'],\
                                        PowerStatusUpdatedBy= SData['data']['PowerStatusUpdatedBy'],\
                                        CTavailable= SData['data']['CTavailable'],\
                                        CTConnected= SData['data']['CTConnected'],\
                                        CTRatio= SData['data']['CTRatio'],\
                                        # = SData['data'][' '],\
                                        DriveTo = TTT, OpenBM = OpenBMHTMLStr if CheckUserAuth(SID,'BMCO') else '', \
                                        MeterByPass = ByPassMeterHTMLStr if CheckUserAuth(SID,'BPMSD') else '',\
                                        SiteVisitRequest = SiteVisitHTMLStr if CheckUserAuth(SID,'SVCR') else '',\
                                        ALFMeter = "<span> </span><i class='bx bx-message-rounded-check bx-tada' style='color:#33ff00; float: right; font-size: x-large; font-weight: bold;'  ></i>" if IsAlFanarMeter(SData['data']['MeterSN']) else "<span> </span><i class='bx bxs-message-x bx-tada' style='color:red; float: right; font-size: x-large; font-weight: bold;'  ></i>"
                                        ) 


                return render_template("InformationData.html",\
                                        UserName = ActiveSessions[SID]["UserFName"],\
                                        PremiseNumber=SData['data']['Premise'],\
                                        SubscriptionNumber = SData['data']['SubScriptionNum'],\
                                        AccountNumber=SData['data']['AccountNumber'], \
                                        MeterNumber = SData['data']['MeterSN'],\
                                        OfficeNumber=SData['data']['Office'],\
                                        Location=SData['data']['Latitude'] + ', ' + SData['data']['Longitude'] ,\
                                        Technology=SData['data']['Technology'],\
                                        MeterType=SData['data']['MeterType'], \
                                        TarifType= SData['data']['TarifType'], \
                                        PreReading= SData['data']['PreReading'], \
                                        PreReadingDate=SData['data']['PreReadDate'], \
                                        BreakerCapacity =SData['data']['BreakerCapacity'], \
                                        MRU= SData['data']['MRU'],\
                                        EquNum= SData['data']['EquipNum'],\
                                        RSeq= SData['data']['RoutSeq'],\
                                        LBDate= SData['data']['LastBill'],\
                                        BRNumber= SData['data']['BreakerSN'],\
                                        CMNumber= SData['data']['CommModule'],\
                                        DriveTo = TTT, OpenBM = OpenBMHTMLStr if CheckUserAuth(SID,'BMCO') else '', \
                                        MeterByPass = ByPassMeterHTMLStr if CheckUserAuth(SID,'BPMSD') else '',\
                                        SiteVisitRequest = SiteVisitHTMLStr if CheckUserAuth(SID,'SVCR') else '',\
                                        ALFMeter = "<span> </span><i class='bx bx-message-rounded-check bx-tada' style='color:#33ff00; float: right; font-size: x-large; font-weight: bold;'  ></i>" if IsAlFanarMeter(SData['data']['MeterSN']) else "<span> </span><i class='bx bxs-message-x bx-tada' style='color:red; float: right; font-size: x-large; font-weight: bold;'  ></i>"
                                        )
            else:
                #return render_template("MessagePage.html",BColor = "Red", SystemMessage="This meter is out of your coverage areas.", ActionLink="sm", ActionMethod= "GET" )
                return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="This meter is out of your coverage areas.", MsgTitle="Meter Search Application", BackTo= "/sm" )
        else:
            #return render_template("PageNOTFound.html")
            return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="Meter Not found using your search criteria.", MsgTitle="Meter Search Application", BackTo= "/sm" )
            
            
        return SearchKey + '--->' + SearchData
    else:
        resp = make_response(render_template("Login.html", NextPage = "sm"))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route('/sm2sm/open', methods=['POST'])
def CreateSmartToSmartOrder():
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, "/sm2sm"):
            pass
            return "OK"
        else:
            return render_template("MessagePage.html",BColor = "Red", SystemMessage="You don't have authority to open Smart-to-Smart meter replacement.", ActionLink="../", ActionMethod= "GET" )
    else:
        resp = make_response(render_template("Login.html", NextPage = "/sm2sm"))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


@app.route('/bypass/meter' , methods=["POST"])
def DoByPass():
   
    now = datetime.now()
    MNum = request.form.get('MNum2')
    Premise = request.form.get('PNum')
    SID = request.cookies.get('SID')
    UID = ActiveSessions[SID]["UserId"]
   
    ValidTo = now + timedelta(hours=24)
    formatdate = ValidTo.strftime("%Y-%m-%d %H:%M:%S")
    # print('Bypass Request')
    # print(UID,MNum,Premise,ValidTo,formatdate)
    # logger.info('Bypass Request')
    logger.info(str(UID)+str(MNum)+str(Premise)+str(ValidTo)+str(formatdate))

 
    InsertStr = """ Insert into [HES].[dbo].[SAI_NCR_MeterByPass]
                    ([Premise],[MeterNumber],[InsertDate], [InsertedBy],[ValidTo])
                    values
                    ('"""+ Premise +"""','"""+ MNum +"""',getDate(), '"""+ str(UID) +"""','"""+ formatdate+"""')                
                """
    # print(InsertStr)
    try:
        cursor = conn.cursor()
        cursor.execute(InsertStr)
        conn.commit()
    # URL = 'http://t-mwfm.alfanar.com:8090/bypass/add'
    # payload = {
    #             'MNum': MNum
    #           }
    # r = requests.post(URL, data=payload)
    # if r.status_code == 200:
    #     if r.text == "OK":
        return render_template("GeneralMessage.html", MsgTitle="Smart to Smart Application", MSGBody="Your meter ("+ MNum +") has been added to bypass list.", msgcolor = "skyblue", BackTo="../sm")
    except:
        return render_template("GeneralMessage.html", MsgTitle="Smart to Smart Application", MSGBody="Your meter ("+ MNum +") not add to bypass list, error has been occured.", msgcolor = "red", BackTo="../sm")
 
SIMLinks = {
            'SCIR':{'TXT':'''<a href='/hhu/sims/SCIR'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bxs-plane-take-off'></i></div>Request SIMs</button></a><BR>'''},
            'SCR':{'TXT':'''<a href='/hhu/sims/SCR'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bxs-plane-land'></i></div>Return SIMs</button></a><BR>'''},
            'SCIA':{'TXT':'''<a href='/hhu/sims/SCIA'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bx-check-square'></i></div>Apprve Requests</button></a><BR>'''},
            'SCIE':{'TXT':'''<a href='/hhu/sims/SCIE'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bx-transfer-alt'></i></div>Execute request</button></a><BR>'''},
            'SCAR':{'TXT':'''<a href='/hhu/sims/SCAR'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bx-message-alt-dots'></i></div>Request SIM Activation</button></a><BR>'''},
            'SCDCA':{'TXT':'''<a href='/hhu/sims/SCDCA'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bx-mobile-alt'></i></div>Approve device change</button></a><BR>'''},
            'SCRDC':{'TXT':'''<a href='/hhu/sims/SCRDC'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bx-mobile-vibration'></i></div>Request device change</button></a><BR>'''},
            'SCV':{'TXT':'''<a href='/hhu/sims/SCV'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bx-search-alt'></i></div>View SIM card</button></a><BR>'''},
            'SCDA':{'TXT':'''<a href='/hhu/sims/SCDA'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bx-wifi'></i></div>Activate SIM</button></a><BR>'''},
            'SCDD':{'TXT':'''<a href='/hhu/sims/SCDD'><button type="button" class="btn btn-primary"><div class="icon"><i class='bx bx-wifi-off'></i></div>Deactivate SIM</button></a><BR>'''}
           }

@app.route('/hhu/sims', methods=["GET"])
def SimManagementSystem():
    SIMsButtons = ''
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, "/hhu/sims"):
            for X in SIMLinks:
                if CheckUserAuth(SID,X):
                    SIMsButtons = SIMsButtons + SIMLinks[X]['TXT']
            return render_template("SIMManagerMain.html", Btns = SIMsButtons)
        return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="You don't have authority to open SIM card management application.", MsgTitle="SIM Card Application", BackTo= "/hhu/sims" )
    else:
        resp = make_response(render_template("Login.html", NextPage = "/hhu/sims"))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route('/hhu/sims/SCIR', methods=["GET"])
def IssuanceRequest():
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, "/hhu/sims"):
            if CheckUserAuth(SID,'SCIR'):
                return render_template("SIMManagerIssuanceRequest.html")
            else:
                #return render_template("MessagePage.html",BColor = "Red", SystemMessage="You don't have authority to request SIM issuance.", ActionLink="../", ActionMethod= "GET" )
                return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="You don't have authority to request SIM issuance.", MsgTitle="SIM Card Application", BackTo= "/hhu/sims" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="You don't have authority to open SIM card management application.", MsgTitle="SIM Card Application", BackTo= "/hhu/sims" )
    else:    
        resp = make_response(render_template("Login.html", NextPage = "/hhu/sims/SCIR"))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route('/hhu/sims/sendrequest', methods=["POST"])
def IssuanceRequestApply():
    appTxt = "/hhu/sims"
    ThisAuth = 'SCIR'
    ThisRoute = '/hhu/sims/sendrequest'
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                RequestForID = request.form.get('IssueForId')
                RequestForName = request.form.get('IssueForName')
                RequestQty = int(request.form.get('RequestQty'))
                UID = ActiveSessions[SID]["UserId"]
                cursor = conn.cursor()
                SQLIns = "insert into SAI_HHU_SIMs_Requests (RequestBy, RequestDate, ActionType, RequestedQty, RequestForID, RequestForName) values ('"+ str(UID) +"', getdate(), 'issuance', '"+ str(RequestQty) +"', '"+ str(RequestForID) +"','"+ RequestForName +"')"
                cursor.execute(SQLIns)
                conn.commit()
                return render_template("GeneralMessage.html",msgcolor = "SkyBlue", MsgTitle = "SIM Card Issuance Request", MSGBody="Request has been submitted sucessfully, you'll recieve mail after approval.", BackTo="/hhu/sims/SCIR" )
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "SIM Card Issuance Request", MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
                
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "SIM Card Issuance Request", MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp



@app.route('/hhu/sims/SCIA', methods=["GET"])
def ApproveRequests():
    appTxt = "/hhu/sims"
    ThisAuth = 'SCIA'
    ThisRoute = '/hhu/sims/SCIA'
    MTitle = "SIM Card Issuance Approval"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                
                return render_template("SRCSUBForm.html", MyBody=BH.GetHTML_ApproveRequests(conn), PageTitlePy="SIM Card Request Approval") 
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route('/hhu/sims/approverequest', methods=["POST"])
def ApproveRequest():
    appTxt = "/hhu/sims"
    ThisAuth = 'SCIA'
    ThisRoute = '/hhu/sims/SCIA'
    MTitle = "SIM Card Issuance Approval"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                RequestID =  request.form.get('ReqId')
                RequestQty =  request.form.get('ReqQty')
                ActionType =  request.form.get('Action')
                CUID = ActiveSessions[SID]["UserId"]
                if ActionType == 'Approve':
                    SQLStr = "update SAI_HHU_SIMs_Requests set ApprovalStatus=1, ApprovedBy = "+ CUID +", ApproveDate=getdate() , ApprovedQty= "+ RequestQty +" where id =" + RequestID
                else:
                    SQLStr = "update SAI_HHU_SIMs_Requests set ApprovalStatus=0, ApprovedBy = "+ CUID +", ApproveDate=getdate() , ApprovedQty= 0 where id =" + RequestID
                cursor = conn.cursor()
                cursor.execute(SQLStr)
                conn.commit()
                #Send Mail for recieving
                return render_template("SRCSUBForm.html", MyBody=BH.GetHTML_ApproveRequests(conn), PageTitlePy="SIM Card Request Approval")
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp    
#C:\System\SIA\ActiveInv\downloads

@app.route('/downloads/<path:filename>', methods=['GET'])
def downloadfile(filename):
    files = pd.read_sql("select * from SAI_FilesDownloads where [LinkCode]='"+ filename +"'", conn)
    if len(files) > 0 :
        #z="./SAIDUFiles/" + files.iloc[0].ServerFileName
        #print(z)
        #return  send_file(z, attachment_filename=files.iloc[0].ServerFileName)
        # print('File path: ')
        print(os.path.join(app.instance_path, ''))
        logger.debug(os.path.join(app.instance_path))

        return send_from_directory(os.path.join(app.instance_path, ''),files.iloc[0].ServerFileName, as_attachment=True)
    else:
        return render_template("GeneralMessage.html", MsgTitle="Downloading File Failed", msgcolor="red", MSGBody="Wrong link, or you don't have authority to download this file.", BackTo='/' )


#----------------------------------------------------------------------------------------------------
#-------------------------------------------------Burnt Meter--------------------------------
#----------------------------------------------------------------------------------------------------
@app.route('/bm/openbm', methods=["POST"])
def RequestBMOrderCreation():
    appTxt = "/bm"
    ThisAuth = 'SCIA'
    ThisRoute = '/bm/openbm'
    MTitle = "Smart To Smart Meter Replacement"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                Premise = request.form.get('PNum')
                return render_template("SRCSUBForm.html", MyBody=BH.GetHTML_OpenBM(Premise), PageTitlePy=MTitle) 
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp



#----------------------------------------------------------------------------------------------------
#-------------------------------------------------USER Administration--------------------------------
#----------------------------------------------------------------------------------------------------
@app.route("/admin/users/new", methods=["GET"])
def CreateNewUserForm():
    appTxt = "/admin"
    ThisAuth = 'ACNU'
    ThisRoute = '/admin/users/new'
    MTitle = "User Creation"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                return render_template("SRCSUBForm.html", MyBody = BH.GetUserCreationForm(), PageTitlePy="System Administration")
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

#-----------------------------------------------------------------------------------------------------------
@app.route("/admin/users/create" , methods=["POST"])
def CreateNewUser():
    appTxt = "/admin"
    ThisAuth = 'ACNU'
    ThisRoute = '/admin/users/create'
    MTitle = "User Creation"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                NUName = request.form.get('TXTUName')
                NUFName = request.form.get('TXTUFName')
                NULName = request.form.get('TXTULName')
                NUMail = request.form.get('TXTUMail')
                NUMobile = request.form.get('TXTUMobile')
                NUPass = request.form.get('PassCriteria')
                DBUNames = pd.read_sql("Select UserName from HES.dbo.SAI_UserAccount where UserName='"+ NUName +"'", conn)
                if len(DBUNames)==0:
                    if NUPass == "Def":
                        Npassword = "12345678"
                    else:
                        Npassword = "%(#)06d" % {"#" : int(random.random() * 1000000)}
                    encPass = fernet.encrypt(Npassword.encode()).decode()
                    SQLIns = """
                                insert into HES.dbo.[SAI_UserAccount] 
                                    ([UserName],[FirstName],[LastName],[Mail],[MobileNum],[Password],[EnableFlag],[CreatedBy],[CreationDate]) 
                                values 
                                    ('"""+ NUName +"""','"""+ NUFName +"""','"""+ NULName +"""','"""+ NUMail +"""','"""+ NUMobile +"""','"""+ encPass +"""',1,'"""+ ActiveSessions[SID]["UserId"] +"""',getdate())
                            """
                    cursor = conn.cursor()
                    cursor.execute(SQLIns)
                    conn.commit()
                    if NUPass == "Aut":
                        UM.CreateNeSendNewUserMailwUser(NUName,NUFName,NULName,Npassword ,NUMail)
                    


                else:
                    return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="Username ("+ NUName +") already exits.", BackTo="/admin/users/new" )
                
                return render_template("SRCSUBForm.html", MyBody = BH.GetUserCreationForm(), PageTitlePy="System Administration")
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo=appTxt )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route("/admin/users/sysop/<uid>/<actionName>/<parS>" , methods=["POST"])
def systemPassReset(uid, actionName, parS):
    if request.headers["Authorization"] == SystemToken:
        if actionName == "PasswordReset":
            reqD = json.loads(parS)
            if "NewPassword" in reqD.keys():
                NewPassword = reqD["NewPassword"]
            else:
                NewPassword = "%(#)06d" % {"#" : int(random.random() * 1000000)}
            
            


    else:
        return make_response("Token Error", 401)

#-----------------------------------------------------------------------------------------------------------
@app.route("/accman" , methods=["GET"])
def UserAccounP():
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if request.method=="GET":
            return render_template("UserAccount.html", UserName=ActiveSessions[SID]["UserFName"])
        return redirect("/")
    else:    
        resp = make_response(render_template("Login.html", NextPage = "/accman"))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


#-----------------------------------------------------------------------------------------------------------
@app.route("/user/changepass" , methods=["POST","GET"])
def ChangePass():
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if request.method=="GET":
            return render_template("ChangePass.html")
        userData = ActiveSessions[SID]
        UName = userData["UserName"]
        oPass = request.form.get("oldpass")
        nPass1 = request.form.get("psw")
        nPass2 = request.form.get("rpsw")
        if nPass1 == nPass2:
            CHGPass = PasswordChange(UName,oPass,nPass1)
            if CHGPass["Status"]:
                return render_template("GeneralMessage.html",msgcolor = "Lime", MsgTitle = "Password Change", MSGBody="Password has been changed, you'll need to re-login", BackTo="/" )
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "Password Change", MSGBody="Error happened, try again or contact administrator. ("+ CHGPass["Reason"] +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "Password Change", MSGBody="New password don't match re-enter.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = "/user/changepass"))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

#--------------------------------------------------------------------------------
#------------------------------Site Visit----------------------------------------
@app.route('/sitevisit', methods=["GET"])
def SiteVisitApp():
    appTxt = "/sitevisit"
    ThisAuth = 'SVSS'
    ThisRoute = '/sitevisit'
    MTitle = "Site Visit Creation"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                return redirect("/sm")
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

#--------------------------------------------------------------------------------
@app.route('/sitevisit/new', methods=['POST'])
def GoToMySites():
    appTxt = "/sitevisit"
    ThisAuth = 'SVCR'
    ThisRoute = '/sitevisit/new'
    MTitle = "Site Visit Creation"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                UserName = ActiveSessions[SID]["UserFName"]
                PremiseNumber = request.form.get("premise2")
                SubscriptionNumber = request.form.get("SS2")
                AccountNumber = request.form.get("acc2")
                MeterNumber = request.form.get("MNum2")
                Longitude = request.form.get("long2")
                Lattitude= request.form.get("latt2")
                Office = request.form.get("office2")
                # PCDate = request.form.get("PowerConnectionDate") if mtype == "DCU" else ""
                return render_template("SiteVisit.html", UserName=UserName, PremiseNumber=PremiseNumber, SubscriptionNumber=SubscriptionNumber, AccountNumber=AccountNumber, MeterNumber=MeterNumber, Longitude=Longitude, Lattitude=Lattitude, Office=Office )
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


@app.route('/sitevisit/create', methods=['POST'])
def CreateVisitOrder():
    appTxt = "/sitevisit"
    ThisAuth = 'SVCR'
    ThisRoute = '/sitevisit/create'
    MTitle = "Site Visit Creation"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                Office = request.form.get("Office")
                if CheckAreasInAreas(SID,Office, "E"):
                    UserName = "Creating Visit Order"
                    UName = ActiveSessions[SID]["UserName"]
                    PremiseNumber = request.form.get("PNum")
                    SubscriptionNumber = request.form.get("SSNum")
                    AccountNumber = request.form.get("AccNum")
                    MeterNumber = request.form.get("MNum")
                    Longitude = request.form.get("Long")
                    Lattitude= request.form.get("Latt")
                    BG = GFs.GetBusinessGroup(Office, "OM")
                    complainEn = request.form.get("reasonEn")
                    complainAr = request.form.get("reasonAr")
                    requestedBy = request.form.get("requester")
                    print('Site visit created for order: '+str(PremiseNumber))
                    logger.info('Site visit created for order: '+PremiseNumber+' '+complainEn+' '+UName)

                    payload = {
	                            "Premise" : PremiseNumber + '_' + datetime.today().strftime("%Y%m%d"),
	                            "BG" : BG,
	                            "Complaint" : complainEn,
	                            "Office" : Office,
	                            "ComplaintAR" : complainAr,
	                            "Subscription" : SubscriptionNumber,
	                            "accountnumber" : AccountNumber,
	                            "Long" : Longitude,
	                            "Latt" : Lattitude,
	                            "MeterNumber" : MeterNumber,
                                "ReportedBy" : requestedBy,
                                "IssueDate" : datetime.today().strftime("%Y-%m-%d %H:%M"),
                                "CreatedBy" : UName
                              }

                    return render_template("GeneralMessage.html",msgcolor = "lime", MsgTitle = MTitle, MSGBody="Your order has been Created, check in clevest in few seconds.", BackTo="/" ) if GFs.SendToClevest('SVCreate',payload) else render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="Error Happened contact you administrator.", BackTo="/" )
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have access to create site visit in this office.("+ Office +")", BackTo="/" )
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp





@app.route('/sitevisit/createBulk', methods=['POST'])
def CreateVisitOrderBulk():
    # CSV --> JSON [Pnum,reasonEn,requester]
    data = request.json 
    MTitle = "Site Visit Creation"
    for i in data:
        try:
            MyMeter = SECMD[SECMD["Premise"]== i["Pnum"]]
            Office = MyMeter.iloc[0]["Office"]
            PremiseNumber =  MyMeter.iloc[0]["Premise"]
            SubscriptionNumber =  MyMeter.iloc[0]["Subscription No"]
            AccountNumber =  MyMeter.iloc[0]["Account No"]
            MeterNumber = MyMeter.iloc[0]["fg. Ser. No"]
            Longitude =  MyMeter.iloc[0]["Longitude"]
            Lattitude=  MyMeter.iloc[0]["Latitude"]
            BG = GFs.GetBusinessGroup(str(Office), "OM")
            complainEn = i["reasonEn"]
            requestedBy = i["requester"]
            payload = {
                        "Premise" : str(PremiseNumber) + '_' + datetime.today().strftime("%Y%m%d"),
                        "BG" : BG,
                        "Office" : Office,
                        "Subscription" : SubscriptionNumber,
                        "accountnumber" : AccountNumber,
                        "Long" : Longitude,
                        "Latt" : Lattitude,
                        "MeterNumber" : MeterNumber,
                        "ReportedBy" : requestedBy,
                        "Complaint" : complainEn,
                        "IssueDate" : datetime.today().strftime("%Y-%m-%d %H:%M")
                        }
            print(payload)
            GFs.SendToClevest('SVCreate',payload)
        except:
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("A FAIL")
            print(i)
            print(MyMeter)
            print("~~~~~~~~~~~~~~~~~~~~~~~")
    print(str("Done"))
    return render_template("GeneralMessage.html",msgcolor = "lime", MsgTitle = MTitle, MSGBody="Your order has been Created, check in clevest in few seconds.", BackTo="/" )
 
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#ECB

@app.route('/ecb', methods=['GET'])
def ECBRev():
    appTxt = "/ecb"
    ThisAuth = 'RECO'
    ThisRoute = '/ecb'
    MTitle = "ECB Order Revision"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                Uid = ActiveSessions[SID]["UserId"]
                SQL="""select tt.* , (tt.TotalOrders-tt.ClosedOrders) as PendingOrders
                        from (
                                select
                                (select count(premise) from [HES].[dbo].[ECB_ReviseData])  as TotalOrders ,(
                                Select count(premise)  from [HES].[dbo].[ECB_ReviseData] where [InspectionDate] is not null) as ClosedOrders,
                                (Select count(premise) from [HES].[dbo].[ECB_ReviseData] where [InspectionDate] is not null and [UserId]=UUUID) as MyClose) tt
                    """.replace("UUUID", str(Uid))
                TOrdersSummary = json.loads( pd.read_sql(SQL, conn).to_json(orient="index"))["0"]

                return render_template("ECBTemplates/ECBRev.html", TotalOrders= TOrdersSummary["TotalOrders"], TotalClosed=TOrdersSummary["ClosedOrders"], TotalPending=TOrdersSummary["PendingOrders"], MyClosed= TOrdersSummary["MyClose"])
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp




 
    

@app.route('/ecb/getorder', methods=['GET','POST'])
def ECBRevOrder():
    appTxt = "/ecb"
    ThisAuth = 'RECO'
    ThisRoute = '/ecb/getorder'
    MTitle = "ECB Order Revision"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                Uid = ActiveSessions[SID]["UserId"]
                UserOrder = ECR.GetOrderForUser(Uid)
                Photos = []
                for  mphoto in UserOrder["Photos"]["photos"]:
                    Photos.append(mphoto[1:])
                RESP = {
                    "id": UserOrder["id"],
                    "Premise": UserOrder["Premise"],
                    "HON": UserOrder["HON"],
                    "UserId": UserOrder["UserId"],
                    "PickDate": UserOrder["PickDate"],
                    "WNO": UserOrder["WNO"],
                    "SN": UserOrder["SN"],
                    "FinalCompletionDate": UserOrder["FinalCompletionDate"],
                    "Office": UserOrder["Office"],
                    "CON": UserOrder["CON"],
                    "Qustions": ECR.Questions,
                    "Photos": Photos

                }
                #print (RESP)
                json_data = RESP
                images = json_data["Photos"]
                CON=json_data['CON']
                FinalCompletionDate=json_data['FinalCompletionDate']
                HON = json_data['HON']
                Office  = json_data['Office']
                PickDate = json_data['PickDate']
                SN = json_data['SN']
                WNO = json_data['WNO']
                Premise=json_data['Premise']
                UserId= json_data['UserId']
                id=json_data['id']
                ques = json_data['Qustions']
                #return json.dumps(RESP)
                return render_template("pickorder.html", **locals())
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route('/ecb/updaterecord', methods=['POST'])
def UpdateECBData():
    appTxt = "/ecb"
    ThisAuth = 'RECO'
    ThisRoute = '/ecb'
    MTitle = "ECB Order Update after revision"
    SID = request.cookies.get('SID')
    
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                Uid = ActiveSessions[SID]["UserId"]
                oId = request.form.get("id")
                HON = request.form.get("MyHON")
                QestionsAns ={}
                NumberOfNOK = 0
                for i in range(20):
                    try:
                        if request.form.get("Q" + ('0' if i<10 else '')+str(i)) :
                            QestionsAns['INSP0' + ('0' if i<10 else '') + str(i)] = request.form.get("Q" + ('0' if i<10 else '')+str(i))
                            if request.form.get("Q" + ('0' if i<10 else '')+str(i)) == 'n':
                                NumberOfNOK += 1
                    except:
                        print(('0' if i<10 else ''))
                        logger.warning(('0' if i<10 else ''))

                sqlSP = ""
                for pp in QestionsAns.keys():
                    sqlSP += "," + pp + "='"+ QestionsAns[pp] +"' "
                SQLUpdate = "update [HES].[dbo].[ECB_ReviseData] set [InspectionDate]= GETDATE() "+ sqlSP +" where id = '"+ oId +"'"
                #cr = conn.cursor()
                #cr.execute(SQLUpdate)
                #conn.commit()
                ECR.updatetheorder(SQLUpdate)
                #if NumberOfNOK > 0 :
                #    ECR.UnAssignECB(HON)
                return redirect("/ecb")
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#-------------------------Smart To Smart Replacement-----------------------------
#--------------------------------------------------------------------------------


@app.route('/bm/req', methods=['POST','GET'])
def BMRequest():
    appTxt = "/bm"
    ThisAuth = 'BMCO'
    ThisRoute = '/bm/req'
    MTitle = "Site Equipment Replacement"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                #MyMeter = SECMD[SECMD["Premise"]=='4002741047']
                
                #try:
                MyMeter = SECMD[SECMD["Premise"]== request.form.get("PNum")]
                #except:
                #    MyMeter = SECMD[SECMD["Premise"]=='4002741047']

                # print(SECMD.iloc[0])
                # print("My meter"+ str(MyMeter)+" END")
                # print("My meter"+ str(len(MyMeter)))

                if len(MyMeter) > 0 :
                    if IsAlFanarMeter(MyMeter.iloc[0]["fg. Ser. No"]) or IsinByPassList(MyMeter.iloc[0]["Premise"]):
                        Office = MyMeter.iloc[0]["Office"]
                        #print(ActiveSessions[SID])
                        if Office in ActiveSessions[SID]["EAreas"]:
                            PremiseNumber= MyMeter.iloc[0]["Premise"]
                            MeterNumber=MyMeter.iloc[0]["fg. Ser. No"]
                            SubscriptionNumber=MyMeter.iloc[0]['Subscription No']
                            AccountNumber=MyMeter.iloc[0]['Account No']
                            BreakerCapacity=MyMeter.iloc[0]["Breaker Cap."]
                            #cols=['Premise','MRU','Office','fg. Ser. No','Meter Type','Equip. No','Cycle','Last Bill Key','Route Read Seq','MR Note','Date of MR Note','Critical Need','Service Class','Premise Address','City','District','Subscription No','Account No','BPName','BP Type','Latitude','Longitude','Mult. Factor','No. of Dials','Breaker Cap.','Voltage','Phase','Tariff Type','Prev Read Date T','Prev. Read T','Prev Read Date T1','Prev. Read T1','Prev. Read Date T2','Prev. Read T2','Prev Read Date T3','Prev. Read T3','Prev. Read Date T4','Prev. Read T4','Prev. Read Date T5','Prev. Read  T5','Prev. Read Date T6','Prev. Read  T6','Prev. Read Date T7','Prev. Read  T7','Avg. Consp. per day (kWh)','Accl. Premise No','Main Premise No','Conn. Type', 'F1','F2']
                            subreason = BM2BM_Reasons
                            if MyMeter.iloc[0]["Meter Type"] == "DCU":
                                DCUReq = "Y"
                                MeterList=MyMeter.iloc[0]["MeterList"]
                                DCUSerialNumber=MyMeter.iloc[0]["DCUSerialNumber"]
                                TransformerID=MyMeter.iloc[0]["TransformerID"]
                                TransformerRating=MyMeter.iloc[0]["TransformerRating"]
                                PowerConnected=MyMeter.iloc[0]["PowerConnected"]
                                PowerConnectionDate=MyMeter.iloc[0]["PowerConnectionDate"]
                                PowerStatusUpdatedBy=MyMeter.iloc[0]["PowerStatusUpdatedBy"]
                                CTavailable=MyMeter.iloc[0]["CTavailable"]
                                CTConnected=MyMeter.iloc[0]["CTConnected"]
                                CTRatio=MyMeter.iloc[0]["CTRatio"]
                            return render_template('Replacement.html', **locals())
                        else:
                            return  render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You're trying to open order in out of your offices, Premise ("+ request.form.get("PNum") +") in Office ("+ Office +")", BackTo="/" )                            
                    else:
                        return  render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="This meter is not related to Al Fanar.", BackTo="/" )
                        
                else:
                    return  render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="Wrong Entered Premise, Or premise not found.", BackTo="/" )
                 
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#-------------------------Smart To Smart Replacement-----------------------------
#--------------------------------------------------------------------------------
omBGs = {
         '11' : 'OM_Riyadh',
         '14' : 'OM_Riyadh Outer',
         '13' : 'OM_AlKharj',
         '15' : 'OM_Hail',
         '12' : 'OM_Qassim',
         '16' : 'OM_Dawadimi',
         '31' : 'OM_Dammam',
         '33' : 'OM_North_Area',
         '35' : 'OM_Northern_Border',
         '32' : 'OM_Hassa',
         '34' : 'OM_Aljouf'
        }

OrdersForOpen= {}





def RequestHandler():
    conn5 = 'DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T'
    clConn = pyodbc.connect(conn5)
    cr = clConn.cursor()
    global OrdersForOpen
    
    
    
    while True:
        SQL = pd.read_sql("""   Select * from SAI_NCR_Request_Queue where Request_Status = 1  """,clConn)
        print(SQL)

        if len(SQL) > 0:
            print("in if")
            for k,j in SQL.T.iteritems(): 

                HON = str(j['HostOrderNumber'])
                Data = json.loads(j['Source_Data'])
                print(Data)
                global OrdersForOpen
                OrdersForOpen = Data
               
                SQLL = """UPDATE SAI_NCR_Request_Queue set Request_Status = 2 where HostOrderNumber = '"""+HON+"""'  """
                
                print(SQLL)
                re=0
                while re>=0 and re<3:
                    try:
                        cr.execute(SQLL)
                        re = -1 
                    except:
                        re += 1
                        time.sleep(.5)
                    
                clConn.commit()                
        else:
            print("in else")
            print(SQL)
            
                
        
        while len(SQL) == 0:
            
            time.sleep(15)
            SQL = pd.read_sql("""   Select * from SAI_NCR_Request_Queue where Request_Status = 1  """,clConn)
            
t2 = Thread(target=RequestHandler, args=())
t2.daemon = True
t2.start()
if t2.is_alive:

                    print("T2 still alive")
omBGs = {
         '11' : 'OM_Riyadh',
         '14' : 'OM_Riyadh Outer',
         '13' : 'OM_AlKharj',
         '15' : 'OM_Hail',
         '12' : 'OM_Qassim',
         '16' : 'OM_Dawadimi',
         '31' : 'OM_Dammam',
         '33' : 'OM_North_Area',
         '35' : 'OM_Northern_Border',
         '32' : 'OM_Hassa',
         '34' : 'OM_Aljouf'
        }
OrdersForOpen= {}
print(OrdersForOpen)
# Copy Variables
 



def OpenClevestOrders():
    clConn = pyodbc.connect(ClConnectionStr)
    cr = clConn.cursor()
    global OrdersForOpen
    ClevestTargetLink = 'http://mwfm.alfanar.com/MWFM/api/MethodInvocations/SMR_Create?api-version=1'
    Auths = {"UserName" : "sap_api", "Password":"123456"}
    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(Auths["UserName"], Auths["Password"])
    f=open('ddddd.txt','w')
    while True:
        
        while len(OrdersForOpen.keys()) > 0:
            print('Welcome====================>')
            f.write('Welcome====================>\n')
            f.flush()
            inProcess = {}
            myK = ""
            for k in OrdersForOpen.keys():
                inProcess = OrdersForOpen[k]
                myK = k
            f.write(' =======> (2) \n')
            f.flush()
            
            SQLStr = "select HostOrderNumber from WorkOrderMapping where HostOrderNumber like '"+ inProcess["PNum"] +"%' and OrderStatusId not in (100, 80) and ordertypeid in (1,5)"
            runningOrders = pd.read_sql(SQLStr, clConn)
            f.write(' =======> (3) \n')
            f.flush()
            if len(runningOrders) > 0 :
                try:
                    mailIt.SendEmail([inProcess["Mail"]],[],"Replacement Order Creation -"+ inProcess["PNum"] +"-","Other replacement order in progress,\nYour request has been rejected.",[])
                except:
                    pass
                OrdersForOpen.pop(myK, None)

            else:
                MyMeter = SECMD[SECMD["Premise"]== inProcess["PNum"]]

                if MyMeter.iloc[0]["Meter Type"] == "DCU":
                    if len(inProcess["PNum"]) == 20:
                        SQL_NewSer = """select max(convert(int,substring(hostordernumber,23,10))) + 1 as NewSer
                                    from WorkOrderMapping
                                    where HostOrderNumber like '"""+ inProcess["PNum"] +"""-R%'"""
                        # print("TEST-1: "+SQL_NewSer)
                    elif len(inProcess["PNum"]) == 15:
                        SQL_NewSer = """select max(convert(int,substring(hostordernumber,18,10))) + 1 as NewSer
                                    from WorkOrderMapping
                                    where HostOrderNumber like '"""+ inProcess["PNum"] +"""-R%'"""
                        # print("TEST-2: "+SQL_NewSer)
                    else:
                        print("Issue with DCU Premise number" + inProcess["PNum"])
                else:
                    SQL_NewSer = """select max(convert(int,substring(hostordernumber,13,10))) + 1 as NewSer
                                    from WorkOrderMapping
                                    where HostOrderNumber like '"""+ inProcess["PNum"] +"""-R%'"""
                NewHON =(inProcess["PNum"] + '-R{0:07d}').format(pd.read_sql(SQL_NewSer, clConn).fillna(1).iloc[0].NewSer)
                logger.warning("Opening Clevest Order HON: "+NewHON)
                print("Opening Clevest Order HON: "+NewHON)

                #cols=['Premise','MRU','Office','fg. Ser. No','Meter Type','Equip. No','Cycle','Last Bill Key','Route Read Seq','MR Note','Date of MR Note','Critical Need',
                # 'Service Class','Premise Address','City','District','Subscription No','Account No','BPName','BP Type','Latitude','Longitude','Mult. Factor','No. of Dials',
                # 'Breaker Cap.','Voltage','Phase','Tariff Type','Prev Read Date T','Prev. Read T','Prev Read Date T1','Prev. Read T1','Prev. Read Date T2','Prev. Read T2',
                # 'Prev Read Date T3','Prev. Read T3','Prev. Read Date T4','Prev. Read T4','Prev. Read Date T5','Prev. Read  T5','Prev. Read Date T6','Prev. Read  T6',
                # 'Prev. Read Date T7','Prev. Read  T7','Avg. Consp. per day (kWh)','Accl. Premise No','Main Premise No','Conn. Type', 'F1','F2']
                BG = omBGs[inProcess["MeterData"].iloc[0]["Office"][:2]]
                #mD = inProcess["MeterData"]
                f.write(' =======> (4) \n')
                f.flush()
                clMsg = {
                        'BG':BG,
                        'HON':NewHON,
                        'RouteNumber':inProcess["MeterData"].iloc[0]["MRU"],
                        'Office':inProcess["MeterData"].iloc[0]["Office"],
                        'MeterNumber':inProcess["MeterData"].iloc[0]["fg. Ser. No"],
                        'MeterType':inProcess["MeterData"].iloc[0]["Meter Type"],
                        'EquipmentNumber':inProcess["MeterData"].iloc[0]["Equip. No"],
                        'LastReadMonth':inProcess["MeterData"].iloc[0]["Last Bill Key"],
                        'RouteReadSeq':inProcess["MeterData"].iloc[0]["Route Read Seq"],
                        'ServiceClass':inProcess["MeterData"].iloc[0]["Service Class"],
                        'Subscription':inProcess["MeterData"].iloc[0]["Subscription No"],
                        'District':inProcess["MeterData"].iloc[0]["District"],
                        'AccountNumber':inProcess["MeterData"].iloc[0]["Account No"],
                        'CustomerName':inProcess["MeterData"].iloc[0]["BPName"],
                        'Latt':inProcess["MeterData"].iloc[0]["Latitude"],
                        'Long':inProcess["MeterData"].iloc[0]["Longitude"],
                        'Multiplier':inProcess["MeterData"].iloc[0]["Mult. Factor"],
                        'Dials':inProcess["MeterData"].iloc[0]["No. of Dials"],
                        'Breaker':inProcess["MeterData"].iloc[0]["Breaker Cap."],
                        'TarifType':inProcess["MeterData"].iloc[0]["Tariff Type"],
                        'PreRDGDate':inProcess["MeterData"].iloc[0]["Prev Read Date T"],
                        'PreRDG':inProcess["MeterData"].iloc[0]["Prev. Read T"],
                        'AvgConsumption':inProcess["MeterData"].iloc[0]["Avg. Consp. per day (kWh)"],
                        'PremiseAcc':inProcess["MeterData"].iloc[0]["Accl. Premise No"],
                        'PremiseMain':inProcess["MeterData"].iloc[0]["Main Premise No"],
                        'CustomerState':inProcess["MeterData"].iloc[0]["Conn. Type"],
                        'WorkSubType':'RW',
                        'NCR':NewHON,
                        'Premise':inProcess["PNum"],
                        'RepMeter':inProcess["Meter"],
                        'RepComm':inProcess["CM"],
                        'RepECB':inProcess["ECB"],
                        'RepDCU':inProcess["DCU"],
                        'RaisedBy':inProcess["UName"],
                        'Reason' : inProcess["Reason"],
                        'SubReason' : inProcess["SubReason"],
                        'UId' : inProcess["UId"]
                        ,'DCUSerialNumber' : inProcess["MeterData"].iloc[0]["DCUSerialNumber"] if inProcess["DCU"] == 'Y' else ""
                        ,'TransformerID' : inProcess["MeterData"].iloc[0]["TransformerID"] if inProcess["DCU"] == 'Y' else ""
                        ,'TransformerRating' : inProcess["MeterData"].iloc[0]["TransformerRating"] if inProcess["DCU"] == 'Y' else ""
                        ,'PowerConnected' : inProcess["MeterData"].iloc[0]["PowerConnected"] if inProcess["DCU"] == 'Y' else ""
                        ,'PowerConnectionDate' : inProcess["MeterData"].iloc[0]["PowerConnectionDate"] if inProcess["DCU"] == 'Y' else ""
                        ,'PowerStatusUpdatedBy' : inProcess["MeterData"].iloc[0]["PowerStatusUpdatedBy"] if inProcess["DCU"] == 'Y' else ""
                        ,'CTavailable' : inProcess["MeterData"].iloc[0]["CTavailable"] if inProcess["DCU"] == 'Y' else ""
                        ,'CTConnected' : inProcess["MeterData"].iloc[0]["CTConnected"] if inProcess["DCU"] == 'Y' else ""
                        ,'CTRatio' : inProcess["MeterData"].iloc[0]["CTRatio"] if inProcess["DCU"] == 'Y' else ""
                        # ,'SignalStrength' : inProcess["SignalStrength"],
                        # 'MeterList' : inProcess["MeterList"]
                        }
                # f.write(' =======> (32) \n\n\n\n\n')
                # f.flush()
                # f.write('\n\n\n\n\n')
                # f.flush()
                # f.write(str(inProcess["MeterData"]))
                # f.flush()
                # f.write('\n\n\n\n\n')
                # f.flush()
                # f.write(str(clMsg))
                # f.flush()
                # f.write('\n\n\n\n\n')
                # f.flush()
                print(clMsg)
                # print(inProcess["MeterData"])
                # print(inProcess["MeterData"].iloc[0]["Latitude"],)
                # print(inProcess["MeterData"].iloc[0]["Longitude"],)
                # addToClipBoard(str(inProcess["MeterData"]))

                # print(Fore.BLUE + "Order Information: " +Style.RESET_ALL)
                # print(OrdersForOpen)
                # logger.debug(OrdersForOpen)
                # f.write(' =======> (322) \n')
                # f.flush()
                f.write(' =======> (4) \n')
                f.flush()
                resp = requests.post(ClevestTargetLink, data=json.dumps(clMsg),headers=headers,auth=auth)
                if resp.status_code == 200:
                # resp = 200
                # if resp == 200:
                    f.write(' =======> (5) \n')
                    f.flush()
                    print(Fore.GREEN + "Clevest Order"+NewHON+" Created" +Style.RESET_ALL)
                    logger.info("Clevest Order"+NewHON+" Created")

                    try:
                        logger.info("~~~~~~~~TEST~~~~~~~~~~~")
                        f.write(' =======> (6) \n')
                        f.flush()
                        NCRM.CreateMainNCR(clMsg)
                        f.write(' =======> (7) \n')
                        f.flush()
                        print(Fore.GREEN + "NCR Order"+NewHON+" Created" +Style.RESET_ALL)
                    except:
                        f.write(' =======> (8) \n')
                        f.flush()
                        print(Fore.RED + "NCR Order"+NewHON+" Not Created " +Style.RESET_ALL)
                        logger.info("~~~~~~~~TEST~~~~~~~~~~~")

                        print(Fore.RED + "Issue in NCR "+NewHON+" creation" +Style.RESET_ALL)


                    print("order creation mesage: ")
                    print(clMsg)
                    # logger.debug("order creation mesage: ")
                    # logger.debug(clMsg)
                    logger.info("NCR Order"+NewHON+" Created")

                    try:
                        mailIt.SendEmail([inProcess["Mail"]],[],"Replacement Order Creation -"+ inProcess["PNum"] +"-","Dear " + inProcess["FName"] + ",\n    Order has been sent to Clevest, check in few seconds, new HostOrderNumber is ("+ NewHON +").\n\nContact administrator for more information.",[])

                    except:
                        print(Fore.RED + "Mail NOK" +Style.RESET_ALL)
                        logger.error("Mail NOK" + str(inProcess["Mail"]))

                else:
                    try:
                        mailIt.SendEmail([inProcess["Mail"]],[],"Replacement Order Creation -"+ inProcess["PNum"] +"-","Error happened in Clevest, contact admin for more information.",[])
                    except:
                        print(Fore.RED + "Mail NOK" +Style.RESET_ALL)
                        logger.error("Mail NOK" + str(inProcess["Mail"]))

                   


                OrdersForOpen.pop(myK, None)
        
        while len(OrdersForOpen.keys()) == 0:
            time.sleep(15)

t1 = Thread(target=OpenClevestOrders, args=())
t1.daemon = True
t1.start()




def CheckClevest (OrderData):
    print("CheckClevest"+str(OrderData))
    conn2 ='DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T'
    clConn3 = pyodbc.connect(conn2)
    
    clConn2 = pyodbc.connect(ClConnectionStr)

  
    cr1 = clConn3.cursor()
    OrderData['Premise']
    print(OrderData['Premise'])

    SQLStr = """select HostOrderNumber from WorkOrderMapping where HostOrderNumber  ='"""+OrderData['Premise']+"""' """

    runningOrders = pd.read_sql(SQLStr, clConn2)
    print(runningOrders)
    if runningOrders.empty == False:

        print("in IF Created in clevest ")

        NCRM.CreateMainNCR(OrderData)

        SQLL = """UPDATE [HES].[dbo].[SAI_NCR_Request_Queue] set Request_Status = '3' , Clevest_Msg = '"""+json.dumps(OrderData).replace("'", '"')+"""' where HostOrderNumber = """+OrderData['Premise']+"""  """
                
        print(SQLL)
        re=0
        while re>=0 and re<3:
            try:
                cr1.execute(SQLL)
                re = -1 
            except:
                    re += 1
                    time.sleep(.5) 
        clConn3.commit()
        print("Not Empty")

        

        return 201

    elif runningOrders.empty == True:


        time.sleep(5)

        print("in else Created in not clevest ")

        print("Empty")



        CheckClevest(OrderData)
        
        

requestqueue={}
@app.route('/bm/create', methods=['POST','GET'])
def BMCreate():
    appTxt = "/bm"
    ThisAuth = 'BMCO'
    ThisRoute = '/bm/create'
    MTitle = "Site Equipment Replacement"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                if request.form.get("reasons") == None or request.form.get("subreason")==None:
                    return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You must select reason / subreason.", BackTo="/" )
                if request.form.get("Meter") == None and request.form.get("DCU") == None and request.form.get("ECB")  == None and request.form.get("CM") == None :
                    return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You must select at least one device to be replaced.", BackTo="/" )
                PNum = request.form.get("PNum")
                Meter = '' if request.form.get("Meter") == None else request.form.get("Meter")
                DCU = '' if request.form.get("DCU")== None else request.form.get("DCU")
                ECB ='' if  request.form.get("ECB")== None else request.form.get("ECB")
                CM ='' if  request.form.get("CM")== None else request.form.get("CM")
                Reason = request.form.get("reasons")
                SubReason= request.form.get("subreason")
                MyMeter = SECMD[SECMD["Premise"]== request.form.get("PNum")]
                print("SEC DatA "+str(MyMeter))
                print(MyMeter)
                # addToClipBoard(str(MyMeter))
                MyRec = {
                    "PNum":PNum,
                    "Meter" : Meter,
                    "DCU" : DCU,
                    "ECB"  : ECB,
                    "CM" : CM,
                    "MeterData" : MyMeter,
                    "Reason" : Reason,
                    "SubReason" : SubReason,
                    "UName" : ActiveSessions[SID]["UserName"],
                    "UId" : ActiveSessions[SID]["UserId"],
                    "Mail" : ActiveSessions[SID]["Mail"],
                    "FName" : ActiveSessions[SID]["UserFName"]
                }
                TransActionID = str(uuid.uuid1())
                global OrdersForOpen
                OrdersForOpen[TransActionID] = MyRec
                if t1.is_alive:
                    print("T! still alive")
                    logger.info("T! still alive")
                else:
                    logger.warning("T! Stopped" + str(ActiveSessions[SID]["UserId"]))
                    print(Fore.YELLOW + "T! Stopped" +Style.RESET_ALL)

                return render_template("GeneralMessage.html",msgcolor = "lime", MsgTitle = MTitle, MSGBody="Your request has been recieved for premise# ("+ PNum +"), you'll recieve e-mail with the result.", BackTo="/sm" )

            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


@app.route('/bm/multiCreate')
def MultiCreateBM():
    appTxt = "/bm"
    ThisAuth = 'CMSS'
    ThisRoute = '/bm/multiCreate'
    MTitle = "Site Multi Equipment Replacement"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                subreason = BM2BM_Reasons
                return render_template('MultiCreate.html',**locals())
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


@app.route('/bm/multiCreate/Upload', methods=['POST'])
def MultiCreateBMUploader():
    appTxt = "/bm"
    ThisAuth = 'CMSS'
    ThisRoute = '/bm/multiCreate/Upload'
    MTitle = "Site Multi Equipment Replacement"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
  
  
                if request.form.get("reasons") == None or request.form.get("subreason")==None:
                    return render_template("GeneralMessage.html",msgcolor = "Red",  MSGBody="You must select reason / subreason.", BackTo="/" )
            

            # FileStorage object wrapper

                DCU = ''
                CM = ''
                ECB = ''
                Meter = '' if request.form.get("Meter") == None else request.form.get("Meter")
                Reason = request.form.get("reasons")
                SubReason= request.form.get("subreason")
                UName = request.form.get("onbehalf")
                file = request.files["file"]      
                #logger.debug(1)

                if file:
                    df = pd.read_csv(file,dtype=str)
                    df.columns = ['Premise']
                    SearchKey ='PRE'
                    logger.debug(2)

       

                    for i,r in df.iterrows():

                        SearchData = str(r.Premise)
                        print(SearchData)
                        # logger.debug(SearchData)

                        SData = SECMD[SECMD["Premise"]==r.Premise]
                        print("SEC DatA "+SECMD["Premise"])
                   
                        print("CSV Premise "+r.Premise)
                        logger.info("CSV Premise "+r.Premise)

                        # print(SData)
                        # logger.debug(SData)
                        # logger.debug()

                        MyRec = {
                                "PNum":SearchData,
                                "MeterData" : SData,
                                "Meter" : Meter,
                                "ECB"  : ECB,
                                "CM" : CM,
                                "DCU" :DCU,
                                "Reason" : Reason,
                                "SubReason" : SubReason,
                                "UName" : '53394',
                                "UId" : '75',
                                # "UName" : ActiveSessions[SID]["UserName"],
                                # "UId" : ActiveSessions[SID]["UserId"],
                                "Mail" : ActiveSessions[SID]["Mail"],
                                "FName" : ActiveSessions[SID]["UserFName"]
                                } 
                        
                        TransActionID = str(uuid.uuid1())
                        OrdersForOpen[TransActionID] = MyRec

                        print(MyRec)
                         
                        # OpenClevestOrders()

                    return render_template("GeneralMessage.html",msgcolor = "lime", MSGBody="Your request has been recieved , you'll recieve e-mail with the result.", BackTo="/" )
            else:
                    return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------

@app.route('/test', methods=['GET'])
def AA():
    appTxt = "/bm"
    ThisAuth = 'CMSS'
    ThisRoute = '/test'
    MTitle = "Site Multi Equipment Replacement"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):

                return render_template("ConnectionDevice.html")

            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


@app.route('/hes/SIMInfo', methods=['GET'])
def simDataReq():
    appTxt = "/hes"
    ThisAuth = 'CMSS'
    ThisRoute = '/hes/SIMInfo'
    MTitle = "SIM Information"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):

                return render_template("ConnectionDevice.html", tables=pd.DataFrame())

            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


 
@app.route('/hes/SIMInfo/Get', methods=['POST','GET'])
def simDataRetrival():
    appTxt = "/hes"
    ThisAuth = 'CMSS'
    ThisRoute = '/hes/SIMInfo'
    MTitle = "SIM Information"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                SQLstr = """SELECT  
                                DeviceId,
                                CONVERT(varchar,IMSI) as IMSI,
                                CONVERT(varchar,ICCID)  as ICCID   
                            FROM 
                                HES.dbo.SEC_LinkSIM
                            WHERE  
                                SEARCHMETHODPLACEHOLDER IN ('SEARCHMETERPLACEHOLDER')"""
                requestType = request.form.get('reqType')

                if requestType == 'S':
                        searchmethod =  str(request.form.get("searchmethod"))
                        SIMInfoList=  request.form.get("SCriteria")
                        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=clevest;PWD=!C13ve$T')
                        SQLstr= pd.read_sql(SQLstr.replace("SEARCHMETHODPLACEHOLDER",searchmethod).replace("SEARCHMETERPLACEHOLDER",SIMInfoList),conn)
                        conn.close()
                        return render_template('ConnectionDevice.html', tables=SQLstr, titles=SQLstr.columns.values)

                else:
                    searchmethod =  str(request.form.get("searchmethodM"))
                    fileName = request.files['ufile'].filename
                    splitInput = fileName.split('.')
                    if splitInput[1] != "csv":
                        return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "Invalid File Format", MSGBody="file not in the required format. Must be CSV format", BackTo="/hes/SIMInfo" )
                    SIMInfo= pd.read_csv(request.files['ufile'])
                    if len(SIMInfo) > 0:
                            if (len(list(SIMInfo.columns)) > 1)  :
                                print("file not in the required format....")
                                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "Invalid File Format", MSGBody="file not in the required format....", BackTo="/hes/SIMInfo" )
                            else:
                                SIMInfo.columns=[searchmethod]
                    else:
                            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "No Meters in File", MSGBody="There was no Meter entered", BackTo="/hes/SIMInfo" )
                    SIMInfoList = SIMInfo[searchmethod].to_string(index=False)
                    SIMInfoList = SIMInfoList.replace("\n","','")

                    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=clevest;PWD=!C13ve$T')
                    SQLstr= pd.read_sql(SQLstr.replace("SEARCHMETHODPLACEHOLDER",searchmethod).replace("SEARCHMETERPLACEHOLDER",SIMInfoList),conn)
                    conn.close()
                    resp = make_response(SQLstr.to_csv(index = False))
                    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
                    resp.headers["Content-Type"] = "text/csv"
                    return resp
                # return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="Printed", BackTo="/" )

            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


@app.route('/goo', methods=["GET"])
def goo():
    # return render_template("home.html")
    # return render_template("home2.html")
    return render_template("AllApplication2.html")



@app.route("/bar",methods=['GET','POST'])
def data_page():
    
    if request.method == 'POST':
        filesDict = request.files.to_dict()
        uploadData=request.files['media']
        data_file_name = uploadData.filename
        uploadData.save(os.path.join(app.root_path,'uploads\\'+data_file_name))

    return render_template("upload.html")



@app.route("/home",methods=['GET','POST'])
def data_page2():
    return render_template("Restarting.html")

@app.route('/progress')
def progress():
    def generate():
        global SECMD 
        SECfiles = glob.glob( "SECMasterData/*.txt")
        li=[]
        i=5
        for filename in SECfiles:
                yield "data:" + str(i) + "\n\n"
                dfx = pd.read_csv(filename,delimiter=';',header=None, dtype=str,encoding = "utf-8",quoting=csv.QUOTE_NONE)
                i+=1
                # print ('\r |' + ('#' * i) + ('-' * (len(SECfiles) - i)) + '| File loaded -- > ' + filename , end='')
                li.append(dfx)
        SECMD =  pd.concat(li, axis=0, ignore_index=True)
        cols=['Premise','MRU','Office','fg. Ser. No','Meter Type','Equip. No','Cycle','Last Bill Key','Route Read Seq','MR Note','Date of MR Note','Critical Need','Service Class','Premise Address','City','District','Subscription No','Account No','BPName','BP Type','Latitude','Longitude','Mult. Factor','No. of Dials','Breaker Cap.','Voltage','Phase','Tariff Type','Prev Read Date T','Prev. Read T','Prev Read Date T1','Prev. Read T1','Prev. Read Date T2','Prev. Read T2','Prev Read Date T3','Prev. Read T3','Prev. Read Date T4','Prev. Read T4','Prev. Read Date T5','Prev. Read  T5','Prev. Read Date T6','Prev. Read  T6','Prev. Read Date T7','Prev. Read  T7','Avg. Consp. per day (kWh)','Accl. Premise No','Main Premise No','Conn. Type', 'F1','F2']
        SECMD.columns=cols
        # SECMD = pd.concat([SECMD, df], ignore_index=True)
        SECMD = SECMD.fillna('')
        SECMD['fg. Ser. No']= SECMD['fg. Ser. No'].str.upper()
        GMD.SECMDHere = SECMD

    return Response(generate(), mimetype= 'text/event-stream')
# data_page2() 
# @app.route("/home",methods=['GET','POST'])
# def data_page2():
#     return render_template("Restarting.html")

# @app.route('/progress')
# def progress():
#     def generate():
#         global SECMD 
#         SECfiles = glob.glob( "SECMasterData/*.txt")
#         li=[]
#         i=5
#         for filename in SECfiles:
#                 yield "data:" + str(i) + "\n\n"
#                 dfx = pd.read_csv(filename,delimiter=';',header=None, dtype=str,encoding = "utf-8",quoting=csv.QUOTE_NONE)
#                 i+=1
#                 # print ('\r |' + ('#' * i) + ('-' * (len(SECfiles) - i)) + '| File loaded -- > ' + filename , end='')
#                 li.append(dfx)
#         SECMD =  pd.concat(li, axis=0, ignore_index=True)
#         cols=['Premise','MRU','Office','fg. Ser. No','Meter Type','Equip. No','Cycle','Last Bill Key','Route Read Seq','MR Note','Date of MR Note','Critical Need','Service Class','Premise Address','City','District','Subscription No','Account No','BPName','BP Type','Latitude','Longitude','Mult. Factor','No. of Dials','Breaker Cap.','Voltage','Phase','Tariff Type','Prev Read Date T','Prev. Read T','Prev Read Date T1','Prev. Read T1','Prev. Read Date T2','Prev. Read T2','Prev Read Date T3','Prev. Read T3','Prev. Read Date T4','Prev. Read T4','Prev. Read Date T5','Prev. Read  T5','Prev. Read Date T6','Prev. Read  T6','Prev. Read Date T7','Prev. Read  T7','Avg. Consp. per day (kWh)','Accl. Premise No','Main Premise No','Conn. Type', 'F1','F2']
#         SECMD.columns=cols
#         # SECMD = pd.concat([SECMD, df], ignore_index=True)
#         SECMD = SECMD.fillna('')
#         SECMD['fg. Ser. No']= SECMD['fg. Ser. No'].str.upper()
#         GMD.SECMDHere = SECMD

#     return Response(generate(), mimetype= 'text/event-stream')


# @app.route('/progress2')
# def progress2():

#     def generate():
#         x = 0
#         while x <= 100:
#             yield "data:" + str(x) + "\n\n"
#             x = x + 10
#             time.sleep(0.5)
#     return Response(generate(), mimetype= 'text/event-stream')






@app.route('/dummy')
def dummy():
    appTxt = "/dummy"
    ThisAuth = 'XXXX'
    ThisRoute = 'dummy/sub'
    MTitle = "DUMMY"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):

                return render_template('ServicePage.html')

            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------

@app.route('/SIMSiteLinkage ', methods = ['GET'])
def getSIM():
    appTxt = "/SIMSiteLinkage"
    # ThisAuth ='AAAA'
    ThisRoute = '/SIMSiteLinkage'
    MTitle = "Site SIM Linkage"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        # if CheckAppInSession(SID, appTxt):
            # if CheckUserAuth(SID, ThisAuth):

                return render_template('SiteSIMLinkage.html')
            # else:
            #     return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        # else:
        #     return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


@app.route('/SIMSiteLinkage/UploadSIMLink', methods = ['POST'])
def AddSIM():
    appTxt = "/SIMSiteLinkage"
    # ThisAuth ='AAAA'
    ThisRoute = '/SIMSiteLinkage/UploadSIMLink'
    MTitle = "Site SIM Linkage"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        # if CheckAppInSession(SID, appTxt):
            # if CheckUserAuth(SID, ThisAuth):

                # TODO: Upload to DB

                pass

            # else:
            #     return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        # else:
        #     return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------





@app.route('/som/request', methods=['GET'])
def BB_1():
    df = pd.read_csv("templates/assets/docs/Alarms.csv")
    return render_template("SOM_Upload1.html", alarms = df)

def FuncAddCounter(Offset, df):
    print(Offset,)
    ii = Offset
    #Xi = list(range(ii+1, len(df)+1 ))
    Xi = []
    dd = 0
    for tg in range(len(df)):
        dd+=1
        Xi.append(ii + dd)
        
    df["TicketNumber"] = Xi
    return df , (ii+dd)



@app.route('/som/createrequest', methods=['POST'])
def BB_2():
# Confirm the following
# File is CSV format
# alarm 4 contain all CM's for meters
# Missing file created for mesiing only (does not halt the process)
# Confirm that an alarm is selected 
# confirm single is uploaded correctly 
# 
    requestType = request.form.get('reqType')
    if requestType == 'S':
        MultiMeterNo = pd.DataFrame()
        alarmSelected = request.form.get('singleAlarm')
        if alarmSelected == "4":
            splitInput = request.form.get('MeterNo').split(',')
            MultiMeterNo["Meters"] = splitInput[0]
            MultiMeterNo["CMNum"] = splitInput[1]
        MultiMeterNo["Meters"]=[request.form.get('MeterNo')]
        fileName = "MeterList.csv"

    else:
        fileName = request.files['ufile'].filename
        splitInput = fileName.split('.')
        print(splitInput) 
        print(splitInput[0]) 
        print(splitInput[1]) 
        if splitInput[1] != "csv":
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "Invalid File Format", MSGBody="file not in the required format. Must be CSV format", BackTo="/som/request" )



        MultiMeterNo= pd.read_csv(request.files['ufile'])
        alarmSelected = request.form.get('multiAlarm')



    if len(MultiMeterNo) > 0:
        if (len(list(MultiMeterNo.columns)) > 2)  :
                print("file not in the required format....")
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "Invalid File Format", MSGBody="file not in the required format....", BackTo="/som/request" )
        else:
                if (len(list(MultiMeterNo.columns)) == 1):
                    # if alarmSelected == "4" :
                    #     return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "Missing Communication Modules", MSGBody="Missing Communication Module Numbers. Add CM Serials Numbers", BackTo="/som/request" )
                    MultiMeterNo["CMNum"] = ''
                MultiMeterNo.columns=["Meters","CMNum"]
    else:
        return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "No Meters in File", MSGBody="There was no Meter entered", BackTo="/som/request" )


    df = pd.read_csv("templates/assets/docs/Alarms.csv")
    df["id"] =df["id"].astype('str')
    if alarmSelected == None:
        return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "Select Alarm", MSGBody="Select alarm type before proceeding", BackTo="/som/request" )
    reqAlarm = df[df["id"] == alarmSelected]
    Al, ALAgg , DevType = reqAlarm.iloc[0]["Alarm"], reqAlarm.iloc[0]["Key"], reqAlarm.iloc[0]["DevType"]
    
    if DevType == "Meter":
        global SECMD
        df_Main=pd.DataFrame()
        df_Main = SECMD[SECMD["fg. Ser. No"].isin(MultiMeterNo["Meters"])]
        df_Main = pd.merge(df_Main,MultiMeterNo, how='inner', left_on='fg. Ser. No', right_on='Meters' )
        print(df_Main)
        print(df_Main.columns)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        df_Main = df_Main[['Premise','fg. Ser. No','Office','MRU','Equip. No','Cycle','Subscription No','Account No','Latitude','Longitude','Breaker Cap.','Avg. Consp. per day (kWh)','CMNum']]
        df_Main["Latitude"] = df_Main["Latitude"].str[:10]
        df_Main["Longitude"] = df_Main["Longitude"].str[:10]
        df_Main['MeterReadDateTime']=""
        df_Main = df_Main[:]
        df_Main = df_Main.reset_index()
        print("Orders ---> " + str(len(df_Main)))
        LastTicketNumber = pd.read_csv("templates/assets/docs/LastTicketNum.csv").iloc[0]["Num"]
        df_Main , LastTicketNumber = FuncAddCounter(LastTicketNumber, df_Main) 
        df_Main["HostOrderNumber"] = df_Main["Premise"] + "_" + ALAgg
        df_Main["severity"] = 1
        df_Main["Work_type"] = "Meter"
        df_Main["Work_sub_type"] = "Not Connected"
        df_Main["Incident_description"] = Al
        df_Main["Classification"] = "NC"
        df_Main["Device_type"] = "Meter"
        df_Main["SM_count"] = Al
        df_Main["Issue_type"] = "Meter"
        df_Main["MessageID"] = ""
        df_Main['IncCreationTime'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        df_Main["SRC"] = "ALF"
        df_Main["MeterType"]=df_Main["fg. Ser. No"].str[:3]
        df_Main = df_Main.reset_index()
        temp_conn = pyodbc.connect("DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=clevest;UID=DataAnalysisReadOnly;PWD=D2#@J5u2Y3;")
        ClevestData = pd.read_sql("""select SUBSTRING(HostOrderNumber,1,10) as HON, format(count(hostordernumber)+1,'0') as cnt
        from Clevest.dbo.WorkOrderMapping
        where OrderTypeId=13 
        group by SUBSTRING(HostOrderNumber,1,10) """,conn)
        temp_conn.close()
        df_Main=pd.merge(df_Main, ClevestData, left_on='Premise', right_on='HON', how='left')
        df_Main = df_Main.fillna(0)
        df_Main["HostOrderNumber"] = df_Main["HostOrderNumber"] + "_" + df_Main["cnt"].astype(str)
        df_Main["NewTicketNumber"] = ""
        # Why it loops again? it is causing issue during merge the second time round
        
        MultiMeterNo[~MultiMeterNo["Meters"].isin(df_Main["fg. Ser. No"])].to_csv("templates/assets/docs/"+fileName.replace(".csv","_Missing.csv"))
        BGs = pd.read_csv(r"templates/assets/docs/BGs.csv", dtype=str)
        df_Main["Areakey"] = df_Main["Office"].str[:2]
        df_Main = pd.merge(df_Main, BGs, left_on='Areakey' , right_on="ACode", how='left')
        for i, row in df_Main.iterrows():
                print("CNUM: " + str(row["CMNum"]))
                print(row["CMNum"]==None)
                if (alarmSelected == "4") and not row["CMNum"]:
                    return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = "No Meters in File", MSGBody="NCCM alarms must contain a cross-ponding communication module number for each meter.", BackTo="/som/request" )  
                xcc = "ALF{:05d}".format(row["TicketNumber"])
                df_Main.loc[df_Main["HostOrderNumber"]==row["HostOrderNumber"],"NewTicketNumber"] = xcc
                ExpFileName = ALAgg + "_" + datetime.now().strftime('%Y%m%dT%H%M%S') + "_SOMNO.csv"
                df_Main[['HostOrderNumber','severity', 'fg. Ser. No', 'Latitude', 'Longitude','Avg. Consp. per day (kWh)','Cycle','Work_type', 'Work_sub_type', 'Incident_description', 'Breaker Cap.' , 'Account No' ,  'Equip. No', 'MRU', 'Premise', 'Office', "MeterType", 'Classification', 'Device_type', 'BGiD',  'SM_count', 'Issue_type', 'IncCreationTime', 'MeterReadDateTime', 'MessageID', 'NewTicketNumber' , 'Subscription No','SRC','CMNum' ]].to_csv("C:/Users/Maram.Alkhatib/OneDrive - alfanar/Documents/SMP2022/templates/assets/docs/"+ExpFileName, index=False)
                with open("templates/assets/docs/LastTicketNum.csv", 'w') as f:
                    f.write("Num\n")
                    f.write(str(LastTicketNumber))
                print("Process finished. ----> " + ExpFileName)
        path = "templates/assets/docs/"+ fileName.replace(".csv","_Missing.csv" )
        return send_file(path, as_attachment=True)

    else:
        print("DCU")
     
    return render_template("GeneralMessage.html",msgcolor = "kime", MsgTitle = "SOM Tickets Created", MSGBody="SOM Tickets will be created ", BackTo="/som/request" )





@app.route('/um')
def uploadedss():
    #f=open('C:\\System\\SIA\\ActiveInv\\MeterManuData\\numberofmeters.txt')
    #xxx = f.read()
    #f.close()
    return UMD.StartProcess()


@app.route('/hes/files', methods = ['GET'])
def HESFiles():
    appTxt = "/hes"
    ThisAuth = 'HESR'
    ThisRoute = '/hes/files'
    MTitle = "HES Shipment Files Downloader"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                return render_template('MeterDataV2.html')
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route('/hes/download', methods = ['POST'])
def HESFilesdownload():
    appTxt = "/hes"
    ThisAuth = 'HESR'
    ThisRoute = '/hes/download'
    MTitle = "HES Shipment Files Downloader"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                FileType = request.form.get('action')
                Meters = request.form.get('reasonEn')
                MetersList = Meters.split(',')
                Ret = UMD.GenerateShimpentFiles(MetersList,FileType)
                #df = pd.DataFrame(columns=['DEVICE_ID','MANUFACTURER_SERIAL_NUMBER','DEVICE_TYPE','DEVICE_SUBTYPE','DEVICE_MODEL_NUMBER','DEVICE_MANUFACTURER_ABBREVIATION','DEVICE_COMMUNICATION_MOUDLE_MANUFACTURING_YEAR','DEVICE_CALIBRATION_YEAR','DEVICE_PROTOCOL','DEVICE_PROTOCOL_VERSION','DEVICE_MAC_ADDRESS','DEVICE_FIRMWARE_VERSION','DEVICE_CONFIGURATION_VERSION','DEVICE_DISPLAY_REGISTER_DIGIT','DEVICE_COMMUNICATION_TECHNOLOGY','DEVICE_COMMUNICATION_MODULE_MODEL','DEVICE_COMMUNICATION_MODULE_SERIAL_NUMBER','DEVICE_COMMUNICATION_MODULE_MANUFACTURING_YEAR','DEVICE_COMMUNICATION_MODULE_FIRMWARE_VERSION','DEVICE_COMMUNICATION_MODULE_IMEI_NUMBER','DLMS_TCP_PORT','DLMS_COMMUNICATION_PROFILE','DLMS_CLIENT_ID','DLMS_MASTER_KEY','DLMS_AUTHENTICATION_KEY','DLMS_GUC','DLMS_SECURITY_SECRET','DLMS_SECURITY_POLICY','DLMS_AUTHENTICATION_MECHANISM','DLMS_SECURITY_SUITE','COMPANION','COMPANION_VERSION','DEVICE_UTILITYID','UTILITY','INTERNAL_CT_NOMINATOR','INTERNAL_CT_DENOMINATOR','DISCOVER_ID'])
                #df_Comp = pd.DataFrame(Ret["Companion"])
                df_Data = pd.DataFrame(Ret["Data"])
                #for m in Ret["Companion"]:
                #    df.append(m)
                resp = make_response(df_Data.to_csv(index=False, sep=";"))
                resp.headers["Content-Disposition"] = "attachment; filename="+ FileType +".csv"
                resp.headers["Content-Type"] = "text/csv"
                return resp
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp
    

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#----------------------------- NCR Management --------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
@app.route('/ncr',methods=["GET"])
def NCRsTable():
    appTxt = "/ncr"
    ThisAuth = 'VNCR'
    ThisRoute = '/ncr'
    MTitle = "NCR Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                # {"BG": "OM_Riyadh", "HON": "4002348246-R0000004", "RouteNumber": "R1041511", "Office": "1110", "MeterNumber": "KFM2020861227822", "MeterType": "SMD", "EquipmentNumber": "000000000024500364", "LastReadMonth": "2021/10", "RouteReadSeq": "000059", "ServiceClass": "1101", "Subscription": "1141511059", "District": "", "AccountNumber": "010023945291", "CustomerName": " \u0639\u0628\u062f\u0627\u0644\u0631\u062d\u0645\u0646 \u0633\u0644\u064a\u0645\u0627\u0646 \u0639\u0628\u062f\u0627\u0644\u0631\u062d\u0645\u0646 \u0633\u0644\u064a\u0645\u0627\u0646.", "Latt": "24.693900000000", "Long": "46.651400000000", "Multiplier": "1.00000", "Dials": "08", "Breaker": "50.0000000", "TarifType": "1", "PreRDGDate": "20211115", "PreRDG": "22898.0000", "AvgConsumption": "20.3009", "PremiseAcc": "", "PremiseMain": "", "CustomerState": "P", "TransformerID": "", "WorkSubType": "RW", "NCR": "4002348246-R0000004", "Premise": "4002348246", "RepMeter": "Y", "RepComm": "", "RepECB": "", "RepDCU": "", "RaisedBy": "53319", "Reason": "Burnt", "SubReason": "Partially", "UId": "19"}
                userid=ActiveSessions[SID]["UserId"]


                allNCR = pd.read_sql( """SELECT 
                                           NCRNumber,
                                            ST.Status as Status,
                                            JSON_VALUE(NCRFullData, '$.Office') as Office,
                                            Reason,
                                            SubReason,
                                            format(CreationDateTime , 'yyyy-MM-dd HH:mm:ss') as CreationDateTime,
                                            Resposability,
                                            format(RectificationDate , 'yyyy-MM-dd HH:mm:ss') as RectificationDate, 
                                            Concat(CrUA.FirstName, ' ', CrUA.LastName) as Created_By,
                                            LastComment,
                                            (SELECT
                                                COUNT(*)
                                            FROM
                                                HES.dbo.SAI_NCRs
                                            WHERE
                                                MainNCRNumber=NCR.NCRNumber
                                            ) as 'SubNum'
                                            
                                         


FROM

(

    SELECT *, ROW_NUMBER() OVER (PARTITION BY NCRNumber Order by id  DESC) AS rnum

    FROM   HES.dbo.SAI_NCRs 

) as NCR
    
                                            inner join SAI_UserAccount as CrUA on CrUA.id = NCR.CreatedBy
                                            LEFT JOIN HES.dbo.SAI_BM_Reasons as RES on RES.id=NCR.NCRReasonID   
                                            LEFT JOIN HES.dbo.SAI_NCR_Statuses as ST ON ST.id = NCR.Status  
                                        WHERE 
                                             MainNCRNumber IS NULL and NCR.rnum = 1
                                            """+ ((""" """) if CheckUserAuth(SID, 'VANC') else ( """and NCR.CreatedBy ='"""  + userid+"""'""" )) + """ Order by CreationDateTime DESC""", conn)
                # json_list=allNCR.astype(str)
                # json_list = json.loads(json.dumps(list(json_list.T.to_dict().values())))

                allNCR.set_index("NCRNumber", drop=True, inplace=True)
                # allNCR["Reasons"]=allNCR["Reason"]+" , "+allNCR["SubReason"]
                # allNCR["Created By"]=allNCR["FName"]+" "+allNCR["LName"]
                try:
                    NCR= allNCR[['Office',"Status","Reason","SubReason","CreationDateTime","Created_By","Resposability","RectificationDate","LastComment","SubNum"]].to_dict(orient="index")
                except:
                    allNCR=pd.read_sql("""SELECT a.*
                    FROM HES.dbo.SAI_NCRs a
                    JOIN (SELECT NCRNumber,   COUNT(*) as no
                    FROM HES.dbo.SAI_NCRs
                    GROUP BY NCRNumber
                    HAVING count(*) > 1 ) b
                    ON a.NCRNumber = b.NCRNumber""", conn)
                    msgbody=   """<table>
                            <thead>
                            <th>ID</th>
                            <th>NCR Number</th>
                            <th>Status</th>
                            <th>Created By</th>
                            <th>Creation Date</th>
                            <th>RectificationDate</th>
                            </thead>
                            <tbody>
                            """
                    for k,v in allNCR.iterrows():
                        msgbody+="""<tr>
                                        <td>"""+str(v['id'])+"""</td>
                                        <td>"""+str(v['NCRNumber'])+"""</td>
                                        <td>"""+str(v['Status'])+"""</td>
                                        <td>"""+str(v['CreatedBy'])+"""</td>
                                        <td>"""+str(v['CreationDateTime'])+"""</td>
                                        <td>"""+str(v['RectificationDate'])+"""</td>
                                    </tr>"""
                    msgbody += """</tbody>
                                  </table>"""

                    print(Fore.RED +"Duplacted Order: " +Style.RESET_ALL)
                    logger.critical("Duplacted Order:" + str(v['CreatedBy']))

                    mailIt.SendEmail(['maram.alkhatib@alfanar.com','hela.alkudisi@alfanar.com'],[],"Dups Detected",msgbody,[])
                                    # print(NCR)
                RefreshSM2SMReasons()

                subreason = BM2BM_Reasons
                # print(BM2BM_Reasons)

                return render_template("TableAllNCR.html" , Status = statusList, Reason = subreason,NCR=NCR)
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route('/ncr/viewncr/<ncrnum>',methods=["GET"])
def getncr(ncrnum):
    appTxt = "/ncr"
    ThisAuth = 'VNCR'
    ThisRoute = '/ncr'
    MTitle = "NCR Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                allNCR = """SELECT NCRNumber,MainNCRNumber,ST.Status as Status,Reason,SubReason,NCRFullData ,LEFT(CreationDateTime , 12) as 'Creation Date',
                                   uid.FirstName as FName,uid.LastName as LName,NCR.CreatedBy,Premise,Resposability,OESerial as 'Old Device Number',
                                   OERating as 'Old Device Rating',NESerial as 'New Device Number',NERating as 'New Device Rating',
                                   LEFT(RectificationDate , 12) as 'Rectification Date' , RectifiedBy, Invest as 'Investigation Comment', NCRType
                            FROM HES.dbo.SAI_NCRs as NCR
                                LEFT JOIN HES.dbo.SAI_BM_Reasons as RES on RES.id=NCR.NCRReasonID
                                LEFT JOIN HES.dbo.SAI_UserAccount as uid ON uid.id=NCR.CreatedBy
                                LEFT JOIN HES.dbo.SAI_NCR_Statuses as ST ON ST.id = NCR.Status
                            WHERE MainNCRNumber = '""" + ncrnum + """' or NCRNumber = '""" + ncrnum + """'         
                                """
                NCRData = pd.read_sql(allNCR, conn)
                NCRData.set_index("NCRNumber", drop=True, inplace=True)
                NCRData["Reasons"]=NCRData["Reason"]+" , "+NCRData["SubReason"]
                NCRData["Created By"]=NCRData["FName"]+" "+NCRData["LName"]
                
                NCRData["Office"]=NCRData["NCRFullData"].str.split(':').str[4].str.split().str[0]
                NCRData["Office"]=NCRData["Office"].replace({',':"",'"':""},regex=True)
                NCRData["Office"].fillna(method='ffill',inplace=True)
                # print(NCRData["Office"])
                NCR= NCRData[["MainNCRNumber","Status","Reasons","Creation Date","Office","Created By","Premise","Resposability","Old Device Number","Old Device Rating" ,"New Device Number" ,"New Device Rating","Rectification Date","RectifiedBy","Investigation Comment"]].to_dict(orient="index")
                logger.debug(NCR)
                print(NCR)


                Comm = pd.read_sql( """SELECT Comment,NCRNumber,CommentBy,LEFT(date , 12)as 'date',uid.FirstName as FName,uid.LastName as LName FROM HES.dbo.SAI_NCRComments as comm
                LEFT JOIN HES.dbo.SAI_UserAccount as uid ON uid.id=comm.CommentBy
                WHERE NCRNumber = '""" + ncrnum + """' order by date """, conn)
                Comm["CommentBy"]=Comm["FName"]+" "+Comm["LName"]  
                Comm=Comm.astype(str)
                json_list = json.loads(json.dumps(list(Comm.T.to_dict().values())))
                # print(json_list)
                # logger.debug(json_list)

                RefreshSM2SMReasons()
                subreason = BM2BM_Reasons
                try:    
                    file = os.listdir( app.config['UPLOAD_PATH']+ncrnum)      
                except:
                    file = ""
                   
               
                return render_template("ViewNCR.html",NCRs=NCR ,NCRNum=ncrnum,Comment=json_list,Reason = subreason,file=file)
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp




@app.route('/ncr/approvencr/<ncrnum>',methods=["POST","GET"])
def appncr(ncrnum):
    appTxt = "/ncr"
    ThisAuth = 'ANCR'
    ThisRoute = '/ncr/approvencr'
    MTitle = "NCR Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                uid=ActiveSessions[SID]["UserId"]   

                # print(request.form.getlist("confirm-checkbox")[0])
                # print(request.form.get("confirm-checkbox"))
                # print(request.form.get("reasons-select")) 
                # print(request.form.get("subreasons-select")) 

                
                
                MainNCRData = pd.read_sql( """
                                            SELECT 
                                                NCRNumber, Status,Resposability  FROM HES.dbo.SAI_NCRs as NCR
                                                LEFT JOIN HES.dbo.SAI_BM_Reasons as RES on RES.id=NCR.NCRReasonID 
                                            WHERE 
                                                NCRNumber= '""" + ncrnum +"""'""" , conn)  
                MainNCRData=MainNCRData.astype(str)
                MainNCRData = json.loads(json.dumps(list(MainNCRData.T.to_dict().values())))
                print(Fore.GREEN +"Resp: "+MainNCRData[0]['Resposability']+Style.RESET_ALL)
                if MainNCRData[0]['Status'] == '3':

                
                    investComm= request.form.get("investegation-comment")
                    check ='' if  request.form.get("confirm-checkbox")== None else request.form.get("confirm-checkbox")
                    investComm = re.sub(r'[^a-zA-Z0-9 \. \, ]','',investComm)

                    UpdateSql = """ 
                    UPDATE 
                    [HES].[dbo].[SAI_NCRs]
                    SET 
                    [Invest] = '"""+investComm+"""',
                    [ClosedBy] = '"""+uid+"""'
                   ,[CloseDate] = '"""+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"""'"""

                    if check != '':
                        ReasonId = request.form.get("subreasons-select")
                        if request.form.get("reasons-select") == None or request.form.get("subreasons-select")==None:
                            return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="You must select reason / subreason.", BackTo="/ncr" )
                        print("Checked"+str(os.path.exists("templates/NCRs/" + ncrnum +"/"+"SECApproval"+ncrnum+".pdf")))
                        print("SubReason:")
                        print(os.path.join(app.config['UPLOAD_PATH'] + ncrnum ,"SECApproval"+ncrnum+".pdf"))
                        print(int(request.form.get("subreasons-select")))
                        if  (int(request.form.get("subreasons-select"))< 7) and (os.path.exists("templates/NCRs/" + ncrnum +"/SECApproval"+ncrnum+".pdf") == False):
                            return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="You Must Upload SEC Approval", BackTo="/ncr" )
                        UpdateSql +=""", [NCRReasonID] = '"""+ReasonId+"""' , [Resposability] = (SELECT Resp from [HES].[dbo].[SAI_BM_Reasons] WHERE id= '"""+ReasonId+"""')"""
                    else:
                        print(Fore.GREEN +"Resp: "+MainNCRData[0]['Resposability']+Style.RESET_ALL)
                        if  (MainNCRData[0]['Resposability'] == 'SEC') and (os.path.exists("templates/NCRs/" + ncrnum +"/SECApproval"+ncrnum+".pdf") == False):
                            return render_template("GeneralMessage.html",msgcolor = "red", MSGBody="You Must Upload SEC Approval", BackTo="/ncr" )
                    UpdateSubSql = UpdateSql + """,[Status]= 7 WHERE MainNCRNumber = '"""+ncrnum+"""' and CreatedBy ='"""+uid+"""'"""
                    UpdateSql +=""",[Status]= 6 WHERE NCRNumber = '""" + ncrnum +"""' and CreatedBy ='"""+uid+"""'"""
                    
                    # print(UpdateSubSql)
                    # print(UpdateSql)
                    try:
                        # print('In TRY')
                        # print(UpdateSubSql)
                        # print('*********')
                        # print(UpdateSql)
                        cr = conn.cursor()
                        cr.execute(UpdateSubSql)
                        cr.execute(UpdateSql)
                        conn.commit()
                        print(Fore.GREEN +"Approved: "+ncrnum +Style.RESET_ALL)
                        logger.info(str(uid)+" Approved: "+ncrnum )
                        
                        GenDoc.DocumentCreator(ncrnum)
                        print("Printing DOC")
                        logger.info("Printing DOC: "+ncrnum )
                        return render_template("GeneralMessage.html",msgcolor = "lime", MSGBody="NCR Officially Rectified", BackTo="/ncr" )
                    except Exception as e:
                        print("_____________________________________________")
                        print(e)
                        print("_____________________________________________")
                        return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="Issue occurred while processing order "+ncrnum+" Kindly Contact Admin", BackTo="/ncr" )
                elif  MainNCRData[0]['Status'] < '3':
                    return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="Order still in progress", BackTo="/ncr" )
                elif  MainNCRData[0]['Status'] > '3':
                    return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="Order already Approved", BackTo="/ncr" )
                return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="You don't have authority to preform this action", BackTo="ncr" )
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp
 


@app.route('/ncr/insertComm/<ncrnum>',methods=["POST"])
def PostComment(ncrnum):
    appTxt = "/ncr"
    ThisAuth = 'NCRC'
    ThisRoute = '/ncr/insertComm'
    MTitle = "NCR Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                Comment=request.form.get("Comment")
              
                CommentBy=ActiveSessions[SID]["UserId"]

                Comm= {

                    'NCRNumber':ncrnum,
                    'Comment':Comment,
                    'CommentBy':CommentBy}
                    
                def InsertComment(Comm):  
                    InsertComm= """ Insert INTO HES.dbo.SAI_NCRComments
                                    (date,Comment,CommentBy,NCRNumber)

                            values   
                            """
                        
            
                    Comment = Comm["Comment"]
                    CommentBy = Comm["CommentBy"]
                    NCR_Number = Comm["NCRNumber"]
                    InsertCommData =  """
                                (
                                    GETDATE(),
                                '"""+  Comment  +"""','"""+ CommentBy +"""'
                                ,'"""+ NCR_Number +"""'
                                )
                            """
                
                
                
                   
                    global conn
                    cr = conn.cursor()
                    cr.execute(InsertComm + " " + InsertCommData )
                    conn.commit()    
                InsertComment(Comm)  
                return redirect('/ncr')

                
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route("/updatencr", methods=["POST"])
def UpdateNCR():
    Res = NCRM.updateNCRStatus(request.json)
    print("Update Status is : "+str(Res))
    logger.warning("Update Status is : "+str(Res) )

    if Res["Status"]:
        r ={"Response":"OK"}
        return make_response(json.dumps(r),200)
    else:
        if Res["Disc"]=="DBTimeOut":
            r ={"Response":"NOK-DB Issue"}
            print(Fore.RED+'---------------------- DBTimeOut ----------------------: '  +Style.RESET_ALL )
            print(Fore.BLUE+str(request.json) +Style.RESET_ALL)
            logger.critical('---------------------- DBTimeOut ----------------------: ' )
            

           

            return make_response(json.dumps(r),406)
        else:
            r ={"Response":"OK"}
            return make_response(json.dumps(r),200)


@app.route("/Multiupdatencr", methods=["POST"])
def MultiUpdateNCR():
    Res = NCRM.MultiupdateNCRStatus(request.json)
    if Res["Status"]:
        r ={"Response":"OK"}
        return make_response(json.dumps(r),200)
    else:
        if Res["Disc"]=="DBTimeOut":
            r ={"Response":"NOK-DB Issue"}
            return make_response(json.dumps(r),406)
        else:
            r ={"Response":"OK"}
            return make_response(json.dumps(r),200)


@app.route('/ncr/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    appTxt = "/ncr"
    ThisAuth = 'PNCR'
    ThisRoute = '/ncr/download/'
    MTitle = "NCR Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                
                Folder = filename.split('_')
                path="templates/NCRs/" + Folder[0] 

                if os.path.exists(path +"/"+ filename +".docx") :
                    return send_from_directory(path , filename +".docx")
                else:
                     return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="Report Could Not be Downloaded", BackTo="/" )
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp




@app.route('/upload/<NCRNumber>', methods=['POST'])
def upload_files(NCRNumber):

    appTxt = "/ncr"
    ThisAuth = 'UNCA'
    ThisRoute = '/upload/'
    MTitle = "NCR Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):

                print(NCRNumber)
                SECApproval =request.form['flexRadioDefault']
                print(SECApproval)

                uploaded_file = request.files['file']
                filename = secure_filename(uploaded_file.filename)
                
                print(filename)
                if filename != '':
                    file_ext = os.path.splitext(filename)[1]

                    if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
               
                        abort(400)
                    if os.path.exists("templates/NCRs/" + NCRNumber):
                        if SECApproval == 'SECApproval':
                            file_ext = os.path.splitext(filename)[1]
                            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'] + NCRNumber , filename))
                            now1 = datetime.now()
                            dt_string = now1.strftime("%d_%m_%Y_%H_%M_%S")
                            source=app.config['UPLOAD_PATH'] + NCRNumber+"/"+filename
                            destination=app.config['UPLOAD_PATH'] + NCRNumber+"/"+'SECApproval'+NCRNumber+file_ext
                            print (source+"$$"+destination)
                            os.rename(source,destination)

                            
                    else:
                        os.mkdir("templates/NCRs/" + NCRNumber)
                    if SECApproval == 'SECApproval':
                        file_ext = os.path.splitext(filename)[1]

                        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'] + NCRNumber , filename))
                        now1 = datetime.now()
                        dt_string = now1.strftime("%d_%m_%Y_%H_%M_%S")
                        source=app.config['UPLOAD_PATH'] + NCRNumber+"/"+filename
                        destination=app.config['UPLOAD_PATH'] + NCRNumber+"/"+'SECApproval'+"_"+dt_string+file_ext
                        print (source+"$$"+destination)
                        os.rename(source,destination)
        
                    return render_template("GeneralMessage.html",msgcolor = "lime",  MSGBody="File Uploaded Successfully", BackTo="/ncr" )
                else:
                     return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="File Could Not be Uploaded", BackTo="/" )
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp



########Download FIR Report ##############
@app.route('/DownloadReport/<ncr>/<path:filename>',methods=['GET'])
def upload(ncr,filename):
    print(ncr,filename)
    logger.info(str(ncr)+str(filename))

    appTxt = "/ncr"
    ThisAuth = 'PNCR'
    ThisRoute = '/DownloadReport/'
    MTitle = "NCR Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                
                Folder = filename.split('_')
                path="templates/NCRs/" + Folder[0] 

                if os.path.exists(app.config['UPLOAD_PATH']+ncr) :
                    return send_from_directory(app.config['UPLOAD_PATH']+ncr, filename)
                else:
                     return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="Report Could Not be Downloaded", BackTo="/ncr" )
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/ncr" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/ncr" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp





@app.route('/MultiDownload/Upload')
def MultiDownladUploader():
    appTxt = "/ncr"
    ThisAuth = 'PNCR'
    ThisRoute = '/MultiDownload/Upload'
    MTitle = "NCR Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                return render_template('MultiDownload.html')



            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp


@app.route('/MultiDownload' , methods=['POST'])
def MultiDownlad():
    file = request.files["file"]
    # SID = request.cookies.get('SID')
    
    # userid=ActiveSessions[SID]["UserId"]
    
    appTxt = "/ncr"
    ThisAuth = 'PNCR'
    ThisRoute = '/bv MultiDownload'
    MTitle = "NCR Management"
    SID = request.cookies.get('SID')
    userid=ActiveSessions[SID]["UserId"]
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                allNCR = pd.read_sql( """
                        SELECT 
                            NCRNumber,Mail,Concat(CrUA.FirstName, ' ', CrUA.LastName) as Created_By
                        FROM 
                            HES.dbo.SAI_NCRs as NCR
                            inner join SAI_UserAccount as CrUA on CrUA.id = NCR.CreatedBy
                            LEFT JOIN HES.dbo.SAI_NCR_Statuses as ST ON ST.id = NCR.Status  
                        WHERE 
                            MainNCRNumber IS NULL and NCR.CreatedBy = '"""+userid+"""' and NCR.Status =6 """,  conn)
                if allNCR.empty:
                    return render_template("GeneralMessage.html",msgcolor = "red", MSGBody="No matching records for the requested data. Kindly check the status of the FIR orders before submitting.", BackTo="/" )
                else:
                    ListFIR= []
                    Emillist =[allNCR['Mail'][0]]
                    Uname=allNCR['Created_By'][0]
                    logger.warning('Multiple download by '+Uname)
                    print(Uname)
                    dateNOW = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
                    dst_dir = 'templates\\NCRs\\'+"MultiDwonloadFIR_"+userid+dateNOW 
                    print(Emillist)
                    if file:




                        df = pd.read_csv(file,dtype=str)
                        df.columns = ['NCRNumber']
                        AllData = allNCR[allNCR['NCRNumber'].isin(df['NCRNumber'])]
                        NAllData = df[~df['NCRNumber'].isin(allNCR['NCRNumber'])]
                        print("Status Pending:"+str(AllData['NCRNumber']))
                        print("Status Not Pending:"+str(NAllData['NCRNumber']))





                        if os.path.exists("templates/NCRs/"+"MultiDwonloadFIR_"+userid+dateNOW):

                            for i,r in AllData.iterrows():
                                print("NCRs:"+str(r.NCRNumber))
                        
                                ListFIR.append('templates\\NCRs\\'+str(r.NCRNumber)+"\\")
                        
                        
                        
                            for s in ListFIR:

                                dirs = os.listdir(str(s))

                            for f in dirs:
                                print("this is files to be copied "+str(f))

                                shutil.copy(str(s)+f, dst_dir)
                            shutil.make_archive(dst_dir,'zip',dst_dir)
                        else: 
                            try:
                        
                                os.mkdir( 'templates\\NCRs\\'+"MultiDwonloadFIR_"+userid+dateNOW)
                                for i,r in AllData.iterrows():

                                    ListFIR.append('templates\\NCRs\\'+str(r.NCRNumber)+"\\")
                                for s in ListFIR:
                        

                                    dirs = os.listdir(str(s))

                            
                                    for f in dirs:
                                        print("this is files to be copied "+str(f))

                                        shutil.copy(str(s)+f, dst_dir)
                                shutil.make_archive(dst_dir,'zip',dst_dir)

                            except:

                                os.mkdir( 'templates\\NCRs\\'+"MultiDwonloadFIR_"+userid+dateNOW)
                                for i,r in AllData.iterrows():

                                    ListFIR.append('templates\\NCRs\\'+str(r.NCRNumber)+"\\")

                                for s in ListFIR:
                        

                                    dirs = os.listdir(str(s))


                                for f in dirs:
                                    print("this is files to be copied "+str(f))

                                    shutil.copy(str(s)+f, dst_dir)
                                shutil.make_archive(dst_dir,'zip',dst_dir)

                    msgbody = """<h3> Dear Eng """+Uname+"""</h3><h3> Attached is the requested FIR Reports</h3><h3>The following FIRs are not yet approved by responsible Engineer :\n</h3> """
                    msgbody+= """<table>
                    <thead>

                    <th>FIR Number</th>
                    </thead>
                    <tbody>
                    """
                    if NAllData.empty:
                        msgbody= """<h3> Dear Eng. """+Uname+ """</h3><h3> Attached is the requested FIR Reports</h3><p><b><i>This is an automatically generated email – please do not reply to it. If you have any queries regarding your request please contact admin for support<br> Thank You. </i><b/></p> """
                        mailer.SendEmail(Emillist,[],['Maram.alkhatib@alfanar.com'],"Multiple FIR Reports. " + dateNOW, msgbody ,[r'D:\\SAI_System\\templates\NCRs\\MultiDwonloadFIR_'+userid+dateNOW+'.zip'])
                        logger.info('Multiple download nonapproved ncrs')
                        dir_path = r'templates\\NCRs\\'+"MultiDwonloadFIR_"+userid+dateNOW
                        shutil.rmtree(dir_path, ignore_errors=True)
                        print("Deleted '%s' directory successfully" % dir_path)
                        print(msgbody)
                    else:
                        for k,v in NAllData.iterrows():
                            msgbody+="""<tr>

                        <td>"""+str(v['NCRNumber'])+"""</td>

                        </tr>"""
                        msgbody += """</tbody>
                        </table>
                        
                        <br> <p><b><i>This is an automatically generated email – please do not reply to it. If you have any queries regarding your request please contact admin for support<br> Thank You.</i><b/></p>"""

                        print(msgbody)
                        mailer.SendEmail(Emillist,[],['Maram.alkhatib@alfanar.com'],"Multiple FIR Reports. " + dateNOW, msgbody ,[r'D:\\SAI_System\\templates\NCRs\\MultiDwonloadFIR_'+userid+dateNOW+'.zip'])
                        logger.info('Multiple download done')
                        dir_path = r'templates\\NCRs\\'+"MultiDwonloadFIR_"+userid+dateNOW
                        shutil.rmtree(dir_path, ignore_errors=True)
                        print("Deleted '%s' directory successfully" % dir_path)
               
                return render_template("GeneralMessage.html",msgcolor = "lime", MSGBody="Your request has been recieved , you'll recieve e-mail with the result.", BackTo="/" )
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

@app.route('/freesm', methods=["GET"])
def PrmiseTechData():
    return render_template('GSearchMeter.html')



@app.route('/freesm/showTechData', methods=["POST"])
def ShowOrderTechData():
    #SID = request.cookies.get('SID')
    
    SearchKey = request.form.get('searchmethod')
    SearchData = request.form.get('SCriteria')
    SearchSRC = request.form.get('searchsource')
    
    SData = GMD.GetMeterData(SearchKey, SearchData)
    if "data" in SData:
        TTT='http://maps.google.com/maps?daddr='+ SData['data']['Latitude']+','+  SData['data']['Longitude'] +'&amp;ll='
        #print(CheckUserAuth(SID,'SVCR'))
        return render_template("GInformationData.html",\
                                UserName = "Visitor User",\
                                PremiseNumber=SData['data']['Premise'],\
                                SubscriptionNumber = SData['data']['SubScriptionNum'],\
                                AccountNumber=SData['data']['AccountNumber'], \
                                MeterNumber = SData['data']['MeterSN'],\
                                OfficeNumber=SData['data']['Office'],\
                                Location=SData['data']['Latitude'] + ', ' + SData['data']['Longitude'] ,\
                                DriveTo = TTT,\
                                ALFMeter = "<span> </span><i class='bx bx-message-rounded-check bx-tada' style='color:#33ff00; float: right; font-size: x-large; font-weight: bold;'  ></i>" if IsAlFanarMeter(SData['data']['MeterSN']) else "<span> </span><i class='bx bxs-message-x bx-tada' style='color:red; float: right; font-size: x-large; font-weight: bold;'  ></i>"
                                )
    else:
        #return render_template("MessagePage.html",BColor = "Red", SystemMessage="This meter is out of your coverage areas.", ActionLink="sm", ActionMethod= "GET" )
        return render_template("GeneralMessage.html",msgcolor = "Red", MSGBody="Nothing found using your data......", MsgTitle="Site Locator", BackTo= "/freesm" )
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#------------------------- Check AlfMeter -----------------------------
#----------------------------------------------------------------------

@app.route('/AlfMeter', methods=["GET"])
def AlfMeterReq():
    return render_template('AlfMeterSearch.html')

@app.route('/AlfMeter/Check', methods=["POST"])
def CheckAlfMeter():
    SearchKey = request.form.get('searchmethod')
    SearchData = request.form.get('SCriteria')
    SData = GMD.GetMeterData(SearchKey, SearchData)
    if "data" in SData:
        if IsAlFanarMeter(SData['data']['MeterSN']):
            RespAlf= "Alfanar"
        else:
            RespAlf= "SEC"
        return render_template("AlfanarMeterCheck.html",\
                                UserName = "Guest User",\
                                PremiseNumber=SData['data']['Premise'],\
                                MeterNumber = SData['data']['MeterSN'],\
                                OfficeNumber=SData['data']['Office'],\
                                Resp=RespAlf,\
                                ALFMeter = "<span> </span><i class='bx bx-message-rounded-check bx-tada' style='color:#33ff00; float: right; font-size: x-large; font-weight: bold;'  ></i>" if IsAlFanarMeter(SData['data']['MeterSN']) else "<span> </span><i class='bx bxs-message-x bx-tada' style='color:red; float: right; font-size: x-large; font-weight: bold;'  ></i>"
                                )
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#---------------------------- Order Management ------------------------
#----------------------------------------------------------------------

@app.route('/odm', methods=['GET'])
def GetOdf():
    appTxt = "/odm"
    ThisAuth = 'ROPH'
    ThisRoute = '/odm'
    MTitle = "Order Data Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                return render_template('OrderManagement.html')
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp
    
    

@app.route("/oma", methods=['POST'])
def AcceptOrders():
    appTxt = "/odm"
    ThisAuth = 'ROPH'
    ThisRoute = '/oma'
    MTitle = "Order Data Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):

                myF = request.files['ophFile']
                if myF.filename.lower().endswith(".csv"):
                    OpNumber = str(uuid.uuid1()).replace("-","")
                    myF.save("templates/OImages/SRC/" + OpNumber + ".csv")
                    FileData = {"filename" : OpNumber + ".csv",
                                "userName" : ActiveSessions[SID]["UserFName"],
                                "Mail" : ActiveSessions[SID]["Mail"],
                                "UserId" : ActiveSessions[SID]["UserId"],
                                "RequestFile" : myF.filename
                                }
                    GOP.AppendToList(OpNumber, FileData)
                return render_template("GeneralMessage.html",msgcolor = "Lime", MsgTitle = MTitle, MSGBody="Your request has been submitted with number#" + OpNumber + " and it will be processed soon, you'll recieve mail with the result." , BackTo="/odm" )    
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route ('/odm/img/download/<oid>', methods=['GET','POST'])
def downloadorderimages(oid):
    
    appTxt = "/odm"
    ThisAuth = 'ROPH'
    ThisRoute = '/oma'
    MTitle = "Order Data Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                cUID = ActiveSessions[SID]["UserId"]
                NoExtend = ''
                if CheckUserAuth(SID, 'SAPH'):
                    NoExtend = ''
                else:
                    NoExtend =f" and requestor={cUID}"

                #print(f"Select * from SAI_OPDnld where id={oid} " + NoExtend)
                Simages = pd.read_sql(f"Select * from SAI_OPDnld where id={oid} " + ('' if CheckUserAuth(SID, 'SAPH') else f" and requestor={cUID}") , conn)
                if len(Simages) >0:
                    zfSize = os.path.getsize("templates/OImages/" + Simages.iloc[0]["requestnumber"] + '.zip')
                    zfSize = zfSize / ( 1024 * 1024 )
                    if zfSize > 7:
                        reqIP = str(request.remote_addr)
                        if reqIP.startswith("10.90."):
                            if reqIP.startswith("10.90.10."):
                                pass
                            else:
                                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You can't download this request photos throw HHU network..." , BackTo="/odm" )    
                    return send_from_directory(directory="templates/OImages", filename=Simages.iloc[0]["requestnumber"] + '.zip')
                else:
                    return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You are following wrong/expired link or you may don't have access to this link...." , BackTo="/odm" )    
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp

@app.route("/odm/myrequests", methods=['GET'])
def myRequests():
    appTxt = "/odm"
    ThisAuth = 'ROPH'
    ThisRoute = '/odm/myrequests'
    MTitle = "Order Data Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth):
                    UID = ActiveSessions[SID]["UserId"]
                    UserName = ActiveSessions[SID]["UserFName"]
                    SQLData = pd.read_sql(f"Select id, UploadedFile , format(ExpirationDate,'dd-MMM-yyyy') as Expiration, requeststatus as Status from [HES].[dbo].[SAI_OPDnld] where [requestor]={UID}", conn).fillna('')
                    sRows = []
                    K = 1
                    for i, row in SQLData.iterrows():
                        nLine = {
                            "Ser" : str(K),
                            "File" : row.UploadedFile,
                            "id" : row.id,
                            "Expiration" : row.Expiration,
                            "Status" : row.Status
                        }
                        sRows.append(nLine)
                        K+=1
                    print(sRows)
                    #sRowsx = ["s","sp"]
                    return render_template("OrderManDownload.html", UName = UserName, sRowsx= sRows)
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp
    


#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#----------------------------- PLAN Management -------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

@app.route('/plan', methods=['GET'])
def cPlanHTML():
    appTxt = "/plan"
    ThisAuth = 'PMRE'
    ThisRoute = '/plan'
    ThisAuth2 = 'UAAS'
    MTitle = "Plan Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth) or CheckUserAuth(SID, ThisAuth2):
                    UID = ActiveSessions[SID]["UserId"]
                    UserName = ActiveSessions[SID]["UserFName"]
                    cuDate = (datetime.now() + timedelta(days=1)) if int(datetime.now().strftime('%H')) <= PlanEndTime else (datetime.now() + timedelta(days=2))
                    TPiC = "Last hour plan, tomorrow plan will be closed soon.!" if int(datetime.now().strftime('%H')) == PlanEndTime else ("" if int(datetime.now().strftime('%H')) < PlanEndTime else "Tomorrow Plan is closed already....!!!")
                    return render_template("PlanUploader.html", TPIC=TPiC , mnDate = cuDate.strftime('%Y-%m-%d'), mxDate = (cuDate + timedelta(days=7)).strftime('%Y-%m-%d') , cDate = cuDate.strftime('%Y-%m-%d') , data=ActiveSessions[SID]["Auths"])
            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp    

@app.route('/plan/upload', methods=['GET','POST'])
def cPlanCreate():
    if request.method == "GET":
        return redirect("/plan")
    appTxt = "/plan"
    ThisAuth = 'PMRE'
    ThisAuth2 = 'UAAS'
    ThisRoute = '/plan/upload'
    MTitle = "Plan Management"
    SID = request.cookies.get('SID')
    if TestAndExtendSession(SID):
        if CheckAppInSession(SID, appTxt):
            if CheckUserAuth(SID, ThisAuth) or CheckUserAuth(SID, ThisAuth2):
                    UID = ActiveSessions[SID]["UserId"]
                    UserName = ActiveSessions[SID]["UserFName"]
                    mMail = ActiveSessions[SID]["Mail"]
                    
                    if request.form.get("optradio") == "plan":
                        PDate = request.form.get("PlanDate")
                        fname =request.files['csvfile'].filename 
                        dFile =request.files['csvfile']
                        print(PlanEndTime)
                        print(int(datetime.now().strftime('%H')))
                        if (int(datetime.now().strftime('%H')) > PlanEndTime) and (PDate == (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')):
                            MSGCLR = "OrangeRed"
                            TXTComments = "Your file ("+ fname +") has been rejected for ("+ PDate +"), you missed this plan window."
                            TPiC = "Last hour plan, tomorrow plan will be closed soon.!" if int(datetime.now().strftime('%H')) == PlanEndTime else ("" if int(datetime.now().strftime('%H')) < PlanEndTime else "Tomorrow Plan is closed already....!!!")
                            cuDate = (datetime.now() + timedelta(days=1)) if int(datetime.now().strftime('%H')) <= PlanEndTime else (datetime.now() + timedelta(days=2))
                            return render_template("PlanUploader.html", MSGCLR = MSGCLR ,TPIC =TPiC ,TXTComment=TXTComments , mnDate = cuDate.strftime('%Y-%m-%d'), mxDate = (cuDate + timedelta(days=7)).strftime('%Y-%m-%d') , cDate = cuDate.strftime('%Y-%m-%d') , data=ActiveSessions[SID]["Auths"], fData={})
                        df_thisFile = pd.read_csv(dFile, dtype=str, header=None)
                        tDict = { 
                                    "File" : df_thisFile , 
                                    "filename": fname, 
                                    "UserID" : UID ,
                                    "Date" : datetime.strptime(PDate,'%Y-%m-%d') , 
                                    "Mail" : mMail, 
                                    "userfname":UserName}
                        myPM.Plan_NFiles.append(tDict)
                        if myPM.CheckIfProcessIsLive():
                            #print("It is live")
                            pass
                        else:
                            myPM.StartProcess()
                        MSGCLR = "Lime"
                        TXTComments = "You file (" + fname + ") has been recieved, you'll recieve mail with the result..."
                        #print(datetime.now().strftime('%H'))
                        TPiC = "Last hour plan, tomorrow plan will be closed soon.!" if int(datetime.now().strftime('%H')) == PlanEndTime else ("" if int(datetime.now().strftime('%H')) < PlanEndTime else "Tomorrow Plan is closed already....!!!")
                        cuDate = (datetime.now() + timedelta(days=1)) if int(datetime.now().strftime('%H')) <= PlanEndTime else (datetime.now() + timedelta(days=2))
                        return render_template("PlanUploader.html", msgCLR=MSGCLR ,TPIC =TPiC ,TXTComment=TXTComments , mnDate = cuDate.strftime('%Y-%m-%d'), mxDate = (cuDate + timedelta(days=7)).strftime('%Y-%m-%d') , cDate = cuDate.strftime('%Y-%m-%d') , data=ActiveSessions[SID]["Auths"], fData={})
                    else:
                        fname = request.files['csvfileAssign'].filename
                        dFile = request.files['csvfileAssign']
                        df_thisFile = pd.read_csv(dFile, dtype=str, header=None)
                        df_thisFile = df_thisFile[[0,1]]
                        df_thisFile.columns = ["HostOrderNumber", "Worker"]
                        df_thisFile = df_thisFile.drop_duplicates(keep="first", subset=["HostOrderNumber"])
                        orderHosts = ""
                        ocnt = 0
                        for i, row in df_thisFile.iterrows():
                            ocnt += 1
                            if len(orderHosts) == 0 :
                                orderHosts = "'" +  row.HostOrderNumber + "'"
                            else:
                                orderHosts += ",'" +  row.HostOrderNumber + "'"
                        SSQL = """Select HostOrderNumber, format(OrderTypeId,'#') as OrderTypeId, format(OrderStatusId, '#') as OrderStatusId from Clevest.dbo.workordermapping where hostordernumber in (""" + orderHosts + """) """
                        cnx = pyodbc.connect(ClConnectionStr)
                        dta = pd.read_sql(SSQL, cnx)
                        print(SSQL)
                        print(dta)
                        cnx.close()
                        
                        df_thisFile = pd.merge(df_thisFile, dta, right_on='HostOrderNumber', left_on='HostOrderNumber', how='left')
                        df_thisFile["Status"]="Accepted"
                        df_thisFile = df_thisFile.fillna("NaN")
                        
                        df_thisFile.loc[~df_thisFile["OrderStatusId"].isin(['20','40']) , "Status"] = "Rejected - Order Status Not Accepted"
                        df_thisFile.loc[~df_thisFile["OrderTypeId"].isin(["1", '3', '5', '10', '12']) , "Status"] = "Rejected - Order Type not in assignable orders"
                        df_thisFile.loc[df_thisFile["OrderTypeId"]=='NaN' , "Status"] = "Order Not In Clevest"
                        df_accepted = df_thisFile[df_thisFile["Status"]=='Accepted']
                        
                        file_init = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + str(UID) + '_'
                        for key, grp in df_accepted.groupby("OrderTypeId"):
                            grp[["HostOrderNumber", "Worker"]].to_csv(dict_HostExchange[key]["FilePath"] + "/" + dict_HostExchange[key]["FileNameTemplate"].replace('%',file_init) , header=False, index=False)
                        
                        #"1" : {
                        #        "Name" : "MEX"
                        #        ,"FilePath" : "//10.90.10.59/prd/AllHostExchange/SingleUpdateFolder"
                        #        ,"FileNameTemplate" : "%_Assign_MEX.csv"
                        #      }
                        ffData = {}
                        tblRows = []
                        kv = 0
                        for key, grp in df_thisFile.groupby("Status"):
                            kv+=1
                            #print(kv)
                            tblRows.append([kv, key, len(grp)])
                        
                        MSGCLR = "Lime"
                        ffData["tbl"] = tblRows
                        TXTComments = "You file (" + fname + ") has been recieved, Find result as bellow..."
                        #print(datetime.now().strftime('%H'))
                        TPiC = "Last hour plan, tomorrow plan will be closed soon.!" if int(datetime.now().strftime('%H')) == PlanEndTime else ("" if int(datetime.now().strftime('%H')) < PlanEndTime else "Tomorrow Plan is closed already....!!!")
                        cuDate = (datetime.now() + timedelta(days=1)) if int(datetime.now().strftime('%H')) <= PlanEndTime else (datetime.now() + timedelta(days=2))
                        #print(json.dumps(ffData, indent=4))
                        return render_template("PlanUploader.html", msgCLR=MSGCLR ,TPIC =TPiC ,TXTComment=TXTComments , mnDate = cuDate.strftime('%Y-%m-%d'), mxDate = (cuDate + timedelta(days=7)).strftime('%Y-%m-%d') , cDate = cuDate.strftime('%Y-%m-%d') , data=ActiveSessions[SID]["Auths"], fData=ffData)

                        

                        



            else:
                return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
        else:
            return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
    else:    
        resp = make_response(render_template("Login.html", NextPage = ThisRoute))
        resp.set_cookie("LoggedIn","False")
        resp.set_cookie("SID","")
        resp.set_cookie("ExpireDate", "")
        return resp
#import folium
#import webbrowser
#@app.route("/userlocation")
#def getuserlocation():
#    xconn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T')
#    fff = pd.read_sql("""/****** Script for SelectTopNRows command from SSMS  ******/
#            SELECT TOP (1000) [Id]
#                  ,[Timestamp]
#                  ,[WorkerId]
#                  ,[GPSFixDate]
#                  ,[Latitude]
#                  ,[Longitude]
#                  ,[MotionState]
#              FROM [Clevest].[dbo].[WorkerPoint] where WorkerId=979 and Timestamp > format(GETDATE(),'yyyy-MM-dd')""", xconn)
#    xconn.close()
#    m = folium.Map(location=[24.7136, 46.6753], zoom_start=11)
#    for i, row in fff.iterrows():
#        folium.Marker(location=[row.Latitude,row.Longitude], popup="worker").add_to(m)
#    return m.get_root().render()

#app.run(host='0.0.0.0',port=80,debug=False,threaded=True)
app.run(host='0.0.0.0',port=7080 ,debug=True,threaded=True)
#context = ('t-mwfm.alfanar.com.crt','t-mwfm.alfanar.com.key')
#app.run(host='0.0.0.0',port=443,debug=True,threaded=True, ssl_context=context)
