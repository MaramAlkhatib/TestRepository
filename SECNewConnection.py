import csv
import glob
import os
import time
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import json
pd.set_option('display.max_columns', 999)
from datetime import datetime
Reporttime=datetime.now().strftime('%Y%m%d%H%M%S')
import numpy as np
import pyodbc
from pandas import ExcelWriter
from pandas import ExcelFile
import shutil
import warnings
warnings.filterwarnings('ignore')
# import EMailer as mailer
import MultiFilrEmailer as mailer

Emillist = ['Mohamed.Abdulhameed@alfanar.com']
CCList = ['Mohammed.Sabri@alfanar.com','Mostafa.Lashien@alfanar.com','samaa.almukhlif@alfanar.com']
BCCList = ['Maram.alkhatib@alfanar.com','Hela.Alkudisi@alfanar.com']
CurrentDate =datetime.now().strftime('%d-%m-%Y') 
EmailBody="""Dear Eng. Mohamed 


Please find the file after we received the new SEC SAP data for this week  “"""+CurrentDate+"""”."""


print("Done import")
try :
    os.mkdir('SECNewConnection'+CurrentDate)
except:
    os.mkdir('SECNewConnection'+CurrentDate)
#LoadSECData
SECfiles = glob.glob("//10.90.10.70/sceco/MSTR/CMD/*.txt")
li=[]
i=0
for filename in SECfiles:
    dfx = pd.read_csv(filename,delimiter=';',header=None, dtype=str,encoding = "utf-8",quoting=csv.QUOTE_NONE)
    i+=1
    li.append(dfx)
   # print ('#' + filename , end='')
#print ('\r |' + ('#' * i) + ('-' * (len(SECfiles) - i)) + '| All files loaded')
df_SECMD =  pd.concat(li, axis=0, ignore_index=True)
cols=['Premise','MRU','Office','fg. Ser. No','Meter Type','Equip. No','Cycle','Last Bill Key','Route Read Seq','MR Note','Date of MR Note','Critical Need','Service Class','Premise Address','City','District','Subscription No','Account No','BPName','BP Type','Longitude','Latitude','Mult. Factor','No. of Dials','Breaker Cap.','Voltage','Phase','Tariff Type','Prev Read Date T','Prev. Read T','Prev Read Date T1','Prev. Read T1','Prev. Read Date T2','Prev. Read T2','Prev Read Date T3','Prev. Read T3','Prev. Read Date T4','Prev. Read T4','Prev. Read Date T5','Prev. Read  T5','Prev. Read Date T6','Prev. Read  T6','Prev. Read Date T7','Prev. Read  T7','Avg. Consp. per day (kWh)','Accl. Premise No','Main Premise No','Conn. Type', 'F1','F2']
df_SECMD.columns=cols
print("Concating Done")

#Alfanar Meter
#Open connection

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=HO-MWFMDB.alfanar.com,1433;DATABASE=HES;UID=Clevest;PWD=!C13ve$T')
#Load data from DB
df_alfanarmeters = pd.read_sql("select * from alf_meters ",conn)
conn.close()
print("Get Alfanar meters: " + str(len(df_alfanarmeters)) +" Done")

#filter the meters in SAP "Only start with DG"
MData = df_SECMD[df_SECMD["Meter Type"].str.startswith('DG')]
print( str(len(MData)) +" Digital meters Done")


#filter the meters that is not in alfanar range
MData = MData[~MData["fg. Ser. No"].isin(df_alfanarmeters["DeviceID"])]
print(str(len(MData)) +" Not in Alfanar range Done")

#filter the meters that device type in '205','206','207','208'
MData = MData[MData["fg. Ser. No"].str[5:8].isin(['205','206','207','208'])]
print(str(len(MData)) +" Matching rating Done")

MData.to_csv(r"D:\\SAI_System\\SECNewConnection"+CurrentDate+"\\SECNewConnection.csv")
print("Export Done")
print("Done")
dst_dir = 'D:\\SAI_System\\SECNewConnection'+CurrentDate
shutil.make_archive(dst_dir,'zip',dst_dir)
mailer.SendEmail(Emillist,CCList,BCCList,"SEC New Connection - " + CurrentDate , EmailBody ,[r'D:\\SAI_System\\SECNewConnection'+CurrentDate+'.zip'])
shutil.rmtree(dst_dir, ignore_errors=True)
print("Deleted '%s' directory successfully" % dst_dir)


