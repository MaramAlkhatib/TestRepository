import csv
from itertools import groupby
import re
from opcode import opname
import os, random, math, smtplib, ssl, json,  time, glob
from posixpath import split
from flask import Flask, request, flash,  render_template, redirect, make_response, send_from_directory,abort
from pandas.core.frame import DataFrame
from pandas.io import excel
import requests
from requests.auth import HTTPBasicAuth
from pandas.io.sas import sasreader
from werkzeug.utils import secure_filename
from datetime import date, datetime
from datetime import timedelta
from subprocess import Popen
from win32process import DETACHED_PROCESS, THREAD_PRIORITY_TIME_CRITICAL
import pyodbc
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from threading import Thread
from werkzeug.utils import secure_filename
from colorama import Fore, Back, Style
import warnings
warnings.filterwarnings('ignore')

ClConnectionStr = 'DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=Clevest;UID=clevest;PWD=!C13ve$T'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=HES;UID=Clevest;PWD=!C13ve$T')
app = Flask(__name__, static_folder='templates', instance_path='D:\\SAI_System\\downloads')
app.config['UPLOAD_EXTENSIONS'] = ['.docx','.pdf']
app.config['UPLOAD_PATH'] = "templates/NCRs/"


# --------------- HES Reuest Table ----------------

@app.route('/hes/requesttable', methods=["GET"])
def hesrequest():
    # data = pd.read_csv(r"C:\Users\Maram.Alkhatib\OneDrive - alfanar\Documents\Scripts\SMPScripts\TestEnv\reqdf1.csv")
    data = pd.read_sql("""SELECT top(50) TransId, Verb, format(CreationTimeStamp , 'yyyy-MM-dd HH:mm:ss') as CreationTimeStamp, ParentTransId, MSGStatus
            FROM HES_Intlogs
            WHERE ParentTransId IS NULL
            Order by 
            TransId Desc""",conn)
    subdata = pd.read_sql("""SELECT top(3) TransId, Verb, format(CreationTimeStamp , 'yyyy-MM-dd HH:mm:ss') as CreationTimeStamp, ParentTransId, MSGStatus
            FROM HES_Intlogs
            WHERE ParentTransId IS NOT NULL
            Order by 
            TransId Desc""",conn)
    df = pd.merge(data,subdata,left_on="TransId",right_on="ParentTransId")
    df.to_csv("Docs/df_children.csv")
    # data.set_index("TransId", drop=True, inplace=True)
    data=data[["TransId","Verb", "CreationTimeStamp", "MSGStatus"]]
    data.to_json(orient='columns')
    subdata=subdata[["TransId","Verb","CreationTimeStamp","ParentTransId"]]
    subdata.to_json(orient='columns')
    return render_template('HESRequestTable.html', datas = data, subdata = subdata)



@app.route('/hes/requesttabledemo', methods=["GET"])
def hesrequestdemo():
    return render_template('TableDemo.html')

# inboundMSG, HESOutboundMSG,HESReplyError, HESReponseMSG

# --------------- HES_SIMLink ----------------

@app.route('/hes/simLinkConn', methods=["GET"])
def simLinkConn():
    return render_template('HES_SIMLink.html')


# --------------- DCU Dismantle ----------------

@app.route('/hes/dcudismantle', methods=["GET"])
def dcudismantle():
    return render_template('HES_DCUdismantle.html')


@app.route('/hes/dcudismantle/found', methods=["GET"])
def dcuDismSearchResult():
    df = pd.read_sql("""SELECT TOP(20) * FROM [HES].[dbo].[SAI_NCRs] WHERE MainNCRNumber is null""",conn)
    return render_template('HES_DCUdismTable.html', df =df)


@app.route('/hes/dcudismantle/found/requestform', methods=["GET"])
def dcuDismRequestForm():
    return render_template('HES_DCUdismReqForm.html')


# --------------- Actions Main Page ----------------


@app.route('/hes/devices', methods=["GET"])
def devicesManagment():
    return render_template('HES_devicesServices.html')




# @app.route('/----', methods=["GET"])
# def AAAAAAAAAAAAAAA():
#     appTxt = "/hes"
#     ThisAuth = 'AAAA'
#     ThisRoute = '/----'
#     MTitle = "HES - AAAA"
#     SID = request.cookies.get('SID')
#     if TestAndExtendSession(SID):
#         if CheckAppInSession(SID, appTxt):
#             if CheckUserAuth(SID, ThisAuth):
 


#                 return render_template('AAAA.html')
#             else:
#                 return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to do this action.("+ ThisAuth +")", BackTo="/" )
#         else:
#             return render_template("GeneralMessage.html",msgcolor = "Red", MsgTitle = MTitle, MSGBody="You don't have authority to open this application.", BackTo="/" )
            
#     else:    
#         resp = make_response(render_template("Login.html", NextPage = ThisRoute))
#         resp.set_cookie("LoggedIn","False")
#         resp.set_cookie("SID","")
#         resp.set_cookie("ExpireDate", "")
#         return resp

app.run(host='0.0.0.0',debug=True,threaded=True)
