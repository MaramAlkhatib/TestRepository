import pandas as pd
import time
from pandas.io import sql
import DocCreator as GenDoc
import pyodbc, json, uuid
import os
from flask import Flask, request,render_template
from colorama import Fore, Back, Style

ClConnectionStr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=HO-MWFMDB.alfanar.com,1433;DATABASE=Clevest;UID=clevest;PWD=!C13ve$T'
clConn = pyodbc.connect(ClConnectionStr)
cr = clConn.cursor()
NCR_Reasons = pd.read_sql("Select * FROM [HES].[dbo].[SAI_BM_Reasons]", clConn)

EquipmentRating = {
    '000':'200',
    '001':'300',
    '002':'500',
    '003':'800',
    '004':'250',
    '005':'400',
    '006':'600',
    '007':'1000',
    '008':'160',
    '208':'WC100A',
    '207':'WC160A',
    '206':'SMCT',
    '205':'SMCTVT',
    '302':'DCU',
    '209':'Communication Module',
    '203':'Digital SEC Meter',
    '201' : '',
    '204' : '',
    '200' : '',
    '202' : ''

}


def LogNCR(NCRNumber, uID, ActionType, NewStatus, NewEStatus = '0', Disc=''):
    global clConn
    SQLStr = "insert into [HES].[dbo].SAI_NCR_LOGs ([LogDate],[LogBy],[ActionType],[NewStatus],[NewEStatus],[NCRNumber],[Disc]) values (getdate(),"+ str(uID) +", "+ str(ActionType) +", "+ str(NewStatus) +", "+ str(NewEStatus) +", '"+ NCRNumber +"', '"+ Disc +"')"
    #cr = clConn.cursor()
    re=0
    while re>=0 and re<3:
        try:
            cr.execute(SQLStr)
            re = -1
        except:
            re += 1
            time.sleep(.5)
    clConn.commit()

def CreateMainNCR(OrderData):
        global clConn
        NCR_Number = OrderData["NCR"]
        
        InsertStr = """ Insert into [HES].[dbo].[SAI_NCRs]
                                ([NCRNumber],[MainNCRNumber],[Status],[CreationDateTime],[CreatedBy]
                                ,[Premise],[HostOrderNumber],[ClevestStatus],[NCRFullData],[NCRType]
                                ,[OESerial],[OERating],[EStatus]
                                ,[NCRReasonID],[Resposability])
                        values                 
                    """
        #prepare Data
        
        HON = OrderData["HON"]
        UId = OrderData["UId"]
        Premise = OrderData["Premise"]
        RrLine = NCR_Reasons[NCR_Reasons["Reason"]==OrderData["Reason"] ]
        RLine = RrLine[RrLine["SubReason"]==OrderData["SubReason"] ]
        # print(RrLine)
        # print(RLine)
        # print(NCR_Reasons["Reason"])
        # print(OrderData["Reason"])
        # print(RrLine["SubReason"])
        # print(OrderData["SubReason"])
        ReasonID = RLine.iloc[0].id
        Resposability = RLine.iloc[0].Resp

        #MainNCR:
        InsertData = """
                        (
                        '"""+ NCR_Number +"""',Null,1,getdate(),"""+ str(UId) +"""
                        ,'"""+ Premise +"""','"""+ HON +"""',20,'"""+ json.dumps(OrderData).replace("'", "''") +"""',1
                        ,Null,Null,7
                        ,"""+ str(ReasonID) +""",'""" + Resposability + """'
                        )
                    """

        #If Meter
        if OrderData["RepMeter"] == 'Y':
            MeterNumber = OrderData["MeterNumber"]
            InsertData += """,
                        (
                        '"""+ NCR_Number +"""_Meter','"""+ NCR_Number +"""',1,getdate(),"""+ str(UId) +"""
                        ,'"""+ Premise +"""','"""+ HON +"""',20,'',2
                        ,'"""+ MeterNumber +"""','"""+ EquipmentRating[MeterNumber[5:8]] +"""',7
                        ,"""+ str(ReasonID) +""",'""" + Resposability + """'
                        )
                    """
        
        #If Comm
        if OrderData["RepComm"] == 'Y':
            InsertData += """,
                        (
                        '"""+ NCR_Number +"""_COM','"""+ NCR_Number +"""',1,getdate(),"""+ str(UId) +"""
                        ,'"""+ Premise +"""','"""+ HON +"""',20,'',4
                        ,Null,Null,7
                        ,"""+ str(ReasonID) +""",'""" + Resposability + """'
                        )
                    """
            
        #If ECB
        if OrderData["RepECB"] == 'Y':
            InsertData += """,
                        (
                        '"""+ NCR_Number +"""_ECB','"""+ NCR_Number +"""',1,getdate(),"""+ str(UId) +"""
                        ,'"""+ Premise +"""','"""+ HON +"""',20,'',3
                        ,Null,Null,7
                        ,"""+ str(ReasonID) +""",'""" + Resposability + """'
                        )
                    """

        #If DCU
        if OrderData["RepDCU"] == 'Y':
            InsertData += """,
                        (
                        '"""+ NCR_Number +"""_DCU','"""+ NCR_Number +"""',1,getdate(),"""+ str(UId) +"""
                        ,'"""+ Premise +"""','"""+ HON +"""',20,'',5
                        ,Null,Null,7
                        ,"""+ str(ReasonID) +""",'""" + Resposability + """'
                        )
                    """
        folder = NCR_Number
        parent_path = r"templates\\NCRs\\"

        path = os.path.join(parent_path, folder)



        print(path)
        try:

            os.makedirs(path, exist_ok=True)

            print("Directory '%s' created successfully" % folder)

        except OSError as error:

            print("Directory '%s' can not be created")



        print("AFTER NCR Creation")
        #global clConn
        #cr = clConn.cursor()
        print(InsertStr + " " + InsertData )
        re = 0
        while re>=0 and re<3:
            try:
                cr.execute(InsertStr + " " + InsertData )
                re = -1
            except:
                re += 1
                time.sleep(.5)
        
        clConn.commit()
        return{"Status":True, "Disc":"FIR Complete"} 
    

def InsertMessageToDB(MBody):
    mid = uuid.uuid1()
    SQLSt = "insert into [HES].[dbo].[SAI_NCR_InWeb] ([insertdate], [message], [MSGId]) values (getdate(),'"+ json.dumps(MBody) +"', '"+ str(mid) +"')"
    global clConn
    #cr = clConn.cursor()
    print('Message DB inserted InWeb')
    re=0
    while re>=0 and re<3:
        try:
            cr.execute(SQLSt )
            re = -1
        except:
            re += 1
            time.sleep(.5)
    
    
    clConn.commit()
    return mid

def UpdateInboundMessage(MId, status, MBodyTXT=''):
    SQLL = "update [HES].[dbo].[SAI_NCR_InWeb] set [status]='"+ str(status) +"', processdate=getdate(), response = '"+ str(MBodyTXT) +"' where MSGId='"+ str(MId) +"'"
    global clConn
    #cr = clConn.cursor()
    print('Message DB updated InWeb')

    # print(SQLL)
    re=0
    while re>=0 and re<3:
        try:
            cr.execute(SQLL)
            re = -1
        except:
            re += 1
            time.sleep(.5)
    
    clConn.commit()


def updateNCRStatus(OrderData):
    global cr
    MyMid = InsertMessageToDB(OrderData)

    if "NCRNumber" in OrderData and "OrderStatus" in OrderData :
 
        NCR_Number = OrderData["NCRNumber"]
        print("Update Status request for FIR: "+ NCR_Number)
        re=0
        while re>=0 and re<20:
            try:
                NCR = pd.read_sql( """SELECT status FROM HES.dbo.SAI_NCRs WHERE NCRNumber='"""+NCR_Number+"""'""", clConn)
                re = -1
                print(Fore.BLUE + "FIR " + NCR_Number +" fetched"+Style.RESET_ALL)
            except:
                re += 1
                print(Fore.RED + "FIR " + NCR_Number +" could not be fetched "+Style.RESET_ALL + str(re))
                time.sleep(.5)
                
 

        if re >= 20:
            return  {"Status":False, "Disc":"DBTimeOut"}
       
        if len(NCR)>0:
            NCRstatus = NCR.iloc[0]["status"]
 
            if OrderData['OrderStatus'] ==  40  and NCRstatus == 1 :
                 
                UpdateSql = """ UPDATE [HES].[dbo].[SAI_NCRs] SET [Status] = 2 where NCRNumber = '""" + NCR_Number +"""'"""
                #cr = clConn.cursor()
                print(UpdateSql)
                print('Assign order for order: '+ NCR_Number )
                re=0
                while re>=0 and re<3:
                    try:
                        cr.execute(UpdateSql)
                        re = -1 
                        print(Fore.GREEN + "FIR " + NCR_Number +" Updated to INPROGRESS" +Style.RESET_ALL)

                    except:
                        re += 1
                        time.sleep(.5)
                        print(Fore.RED + "FIR "+NCR_Number+" could not be fetched, Updated to INPROGRESS"+Style.RESET_ALL)
                        
                
                clConn.commit()
                UpdateInboundMessage(MyMid,'100', "Order set in progress")
                # AddQ(OrderData,'OK')
                return{"Status":True, "Disc":"Order set in progress"} 


            # CASE: COMPLETE 
            if OrderData['OrderStatus'] ==  100  and NCRstatus in [2,1] :
                print(Fore.MAGENTA + "FIR Complete START: " + NCR_Number +Style.RESET_ALL)
                SQLs = []
                if 'CompletionDate' in OrderData and 'WNO' in OrderData:
                    MainUpdateSql = """ 
                                    UPDATE 
                                        [HES].[dbo].[SAI_NCRs]  
                                    SET 
                                        [RectificationDate] = '""" + OrderData['CompletionDate'] + """',  
                                        [RectifiedBy] = '""" + OrderData['WNO'] + """' , 
                                        [Status] = 3 
                                    where 
                                        NCRNumber = '""" + NCR_Number + """'"""   
                    SQLs.append(MainUpdateSql)
                    
                    if "MeterRep" in OrderData:
                        if OrderData["MeterRep"] in ['Y','y']:
                            print(Fore.BLUE + "FIR MeterRep: " + NCR_Number +Style.RESET_ALL)
                            MeterNESerial = OrderData["NMeter"]
                            try:
                                MeterNERating = EquipmentRating[OrderData["NMeter"][5:8]]
                            except:
                                MeterNERating = "NA"
                            
                            MeterOESerial = OrderData["OMeter"]
                            try:
                                MeterOERating = EquipmentRating[OrderData["OMeter"][5:8]]
                            except:
                                MeterOERating = "NA"

                            MeterSql="""
                                            UPDATE 
                                                [HES].[dbo].[SAI_NCRs]  
                                            SET  
                                                [RectificationDate] = '""" + OrderData['CompletionDate'] + """',  
                                                [RectifiedBy] = '""" + OrderData['WNO'] + """' , 
                                                [Status] = 7, 
                                                [NESerial] = '""" + MeterNESerial + """' ,  
                                                [NERating] = '""" + MeterNERating + """' ,
                                                [OESerial] = '""" + MeterOESerial + """' ,  
                                                [OERating] = '""" + MeterOERating + """' 
                                            where 
                                                NCRNumber = '""" + NCR_Number +"""_Meter'"""
                            SQLs.append(MeterSql)
                            print("---FIR MeterSql Done---")

                    
                    
                    # Communication Module
                 
                    if "CMRep" in OrderData:
                       if OrderData["CMRep"] in ['Y','y']:
                           print(Fore.BLUE + "FIR CMRep: " + NCR_Number +Style.RESET_ALL)
                 
                           
                           CNESerial = OrderData["NCM"]
                           print(CNESerial)
                           try:
                               CNERating = EquipmentRating[OrderData["NCM"][5:8]]
                           except:
                               CNERating = "NA"
                           
                           COESerial = OrderData["OCM"]
                           print(COESerial)
                           try:
                               COERating = EquipmentRating[OrderData["OCM"][5:8]]
                           except:
                               COERating = "NA"
                           CMSql="""
                                           UPDATE 
                                               [HES].[dbo].[SAI_NCRs]  
                                           SET  
                                               [RectificationDate] = '""" + OrderData['CompletionDate'] + """',  
                                               [RectifiedBy] = '""" + OrderData['WNO'] + """' , 
                                               [Status] = 7, 
                                               [NESerial] = '""" + CNESerial + """' ,  
                                               [NERating] = '""" + CNERating + """' ,
                                               [OESerial] = '""" + COESerial + """' ,  
                                               [OERating] = '""" + COERating + """' 
                                           where 
                                               NCRNumber = '""" + NCR_Number +"""_COM'"""
                           SQLs.append(CMSql)
                           print("---FIR CMSql Done---")

                        #    print(CMSql)
                    
                    
                    # ECB 
          
                    if "ECBRep" in OrderData:
                       if OrderData["ECBRep"] in ['Y','y']:
                           print(Fore.BLUE + "FIR ECBRep: " + NCR_Number +Style.RESET_ALL)
                  

                           ENESerial = OrderData["NECB"]
                           try:
                               ECBNERating = EquipmentRating[OrderData["NECB"][5:8]]
                           except:
                               ECBNERating = "NA"
                           
                           EOESerial = OrderData["OECB"]
                           try:
                               EOERating = EquipmentRating[OrderData["OECB"][5:8]]
                           except:
                               EOERating = "NA"
                           ECBSql="""
                                           UPDATE 
                                               [HES].[dbo].[SAI_NCRs]  
                                           SET  
                                               [RectificationDate] = '""" + OrderData['CompletionDate'] + """',  
                                               [RectifiedBy] = '""" + OrderData['WNO'] + """' , 
                                               [Status] = 7, 
                                               [NESerial] = '""" + ENESerial + """' ,  
                                               [NERating] = '""" + ECBNERating + """' ,
                                               [OESerial] = '""" + EOESerial + """' ,  
                                               [OERating] = '""" + EOERating + """' 
                                           where 
                                               NCRNumber = '""" + NCR_Number +"""_ECB'"""
                           SQLs.append(ECBSql)
                           print("---FIR ECBSql Done---")

                    

                    # DCU 

    
                    if "DCURep" in OrderData:
                       if OrderData["DCURep"] in ['Y','y']:
                           print(Fore.BLUE + "FIR DCURep: " + NCR_Number +Style.RESET_ALL)
                      

                           DNESerial = OrderData["NDCU"]
                           try:
                               DCUNERating = EquipmentRating[OrderData["NDCU"][5:8]]
                           except:
                               DCUNERating = "NA"
                           
                           DOESerial = OrderData["ODCU"]
                           try:
                               DOERating = EquipmentRating[OrderData["ODCU"][5:8]]
                           except:
                               DOERating = "NA"
                           DCUSql="""
                                           UPDATE 
                                               [HES].[dbo].[SAI_NCRs]  
                                           SET  
                                               [RectificationDate] = '""" + OrderData['CompletionDate'] + """',  
                                               [RectifiedBy] = '""" + OrderData['WNO'] + """' , 
                                               [Status] = 7, 
                                               [NESerial] = '""" + DNESerial + """' ,  
                                               [NERating] = '""" + DCUNERating + """' ,
                                               [OESerial] = '""" + DOESerial + """' ,  
                                               [OERating] = '""" + DOERating + """' 
                                           where 
                                               NCRNumber = '""" + NCR_Number +"""_DCU'"""
                           SQLs.append(DCUSql)
                           print("---FIR DCUSql Done---")


                    count = 0
                    #cr = clConn.cursor()
                    for SQL_St in SQLs:
                        print(count)
                        print(SQL_St)
                        re=0
                        while re>=0 and re<3:
                            try:
                                cr.execute(SQL_St)
                                re = -1
                                print(Fore.GREEN + "FIR " + NCR_Number +" Order set to Rectefied" +Style.RESET_ALL + str(re))
                     

                            except:
                                re += 1
                                print(Fore.RED + "FIR " + NCR_Number +" could not be fetched" +Style.RESET_ALL + str(re))
                                time.sleep(.5)

                        clConn.commit()
                        count += 1
                    
                    print("FIR is Done :"+NCR_Number + str(count))
                    UpdateInboundMessage(MyMid,'100', "Order Complete")
                    return{"Status":True, "Disc":"Order Complete"} 
                    
                # AddQ(OrderData,'Fail')
                UpdateInboundMessage(MyMid,'20', "Missing key feilds")
                return{"Status":False, "Disc":"Missing key feilds"} 
                
                
 
            # CASE: CANCEL 
            if OrderData['OrderStatus'] ==  80  and NCRstatus in [2,3,1] :
                # if 'CancelReason' in OrderData and 'UId' in OrderData :
                   # CancelDate = OrderData["CloseDate"]
                #    CancelBy = OrderData["UId"]
                #    CancelReason = OrderData["CancelReason"]
                #    UpdateSql = """ UPDATE [HES].[dbo].[SAI_NCRs] SET [Status] = 5 , [CancelDate] =getDate(),  [CancelReason] ='""" + CancelReason +"""',  [CancelBy] ='""" + CancelBy +"""' where NCRNumber = '""" + NCR_Number +"""'"""
                UpdateSql = """ UPDATE [HES].[dbo].[SAI_NCRs] SET [Status] = 1014 , [CancelDate] =getDate() where NCRNumber = '""" + NCR_Number +"""' OR MainNCRNumber ='""" + NCR_Number +"""'"""
                cr = clConn.cursor()
                cr.execute(UpdateSql)
                clConn.commit()
                UpdateInboundMessage(MyMid,'100', "Order cancelled")
                return{"Status":True, "Disc":"Order Complete"} 
            #    AddQ(OrderData,'Fail')
            #    return {"result":"Missing key feilds"}
                
            # AddQ(OrderData,'Fail')
            UpdateInboundMessage(MyMid,'50', "Incorrect status request")
            return{"Status":False, "Disc":"Incorrect status request"}
        UpdateInboundMessage(MyMid,'70', "NCR not created")
        return{"Status":False, "Disc":"NCR not created"}
    UpdateInboundMessage(MyMid,'20', "Missing key feilds")
    return{"Status":False, "Disc":"Missing key feilds"}
   

def MultiupdateNCRStatus(AllOrderData):
    global cr
    AllOrderData= request.json
    print(Fore.BLUE + "Start Multi FIR Update"+Style.RESET_ALL)
    for OrderData in AllOrderData:
        print(Fore.BLUE + "Updating Order: "+OrderData['NCRNumber'] +Style.RESET_ALL)
        print(OrderData)

        if "NCRNumber" in OrderData and "OrderStatus" in OrderData :
            # print('basic conditions met')

            MyMid = InsertMessageToDB(AllOrderData)

            NCR_Number = OrderData["NCRNumber"]
            re=0
            while re>=0 and re<20:
                try:
                    NCR = pd.read_sql( """SELECT status FROM HES.dbo.SAI_NCRs WHERE NCRNumber='"""+NCR_Number+"""'""", clConn)
                    re = -1
                except:
                    re += 1
                    time.sleep(.5)
            if re >= 20:
                return  {"Status":False, "Disc":"DBTimeOut"}
       
            if len(NCR)>0:
                NCRstatus = NCR.iloc[0]["status"]
                if OrderData['OrderStatus'] ==  40  and NCRstatus == 1 :
                 
                    UpdateSql = """ UPDATE [HES].[dbo].[SAI_NCRs] SET [Status] = 2 where NCRNumber = '""" + NCR_Number +"""'"""
                    #cr = clConn.cursor()
                    # print(UpdateSql)
                    re=0
                    while re>=0 and re<3:
                        try:
                            cr.execute(UpdateSql)
                            re = -1 
                        except:
                            re += 1
                            time.sleep(.5)
                    clConn.commit()
                    UpdateInboundMessage(MyMid,'100', "Order set in progress")
                    # AddQ(OrderData,'OK')
                    return{"Status":True, "Disc":"Order set in progress"}
                
                # CASE: COMPLETE 
                if OrderData['OrderStatus'] ==  100  and NCRstatus in [2,1] :
                    # print('in complete if')

                    SQLs = []
                    if 'CompletionDate' in OrderData and 'WNO' in OrderData:
                        MainUpdateSql = """ 
                                    UPDATE 
                                        [HES].[dbo].[SAI_NCRs]  
                                    SET 
                                        [RectificationDate] = '""" + OrderData['CompletionDate'] + """',  
                                        [RectifiedBy] = '""" + OrderData['WNO'] + """' , 
                                        [Status] = 3 
                                    where 
                                        NCRNumber = '""" + NCR_Number + """'"""   
                        SQLs.append(MainUpdateSql)
                        if "MeterRep" in OrderData:
                            if OrderData["MeterRep"] in ['Y','y']:
                                MeterNESerial = OrderData["NMeter"]
                                try:
                                    MeterNERating = EquipmentRating[OrderData["NMeter"][5:8]]
                                except:
                                    MeterNERating = "NA"
                            
                                MeterOESerial = OrderData["OMeter"]
                                try:
                                    MeterOERating = EquipmentRating[OrderData["OMeter"][5:8]]
                                except:
                                    MeterOERating = "NA"
                                MeterSql="""
                                            UPDATE 
                                                [HES].[dbo].[SAI_NCRs]  
                                            SET  
                                                [RectificationDate] = '""" + OrderData['CompletionDate'] + """',  
                                                [RectifiedBy] = '""" + OrderData['WNO'] + """' , 
                                                [Status] = 7, 
                                                [NESerial] = '""" + MeterNESerial + """' ,  
                                                [NERating] = '""" + MeterNERating + """' ,
                                                [OESerial] = '""" + MeterOESerial + """' ,  
                                                [OERating] = '""" + MeterOERating + """' 
                                            where 
                                                NCRNumber = '""" + NCR_Number +"""_Meter'"""
                                SQLs.append(MeterSql)
                        
                        # Communication Module
                 
                        if "CMRep" in OrderData:
                            if OrderData["CMRep"] in ['Y','y']:
                                CNESerial = OrderData["NCM"]
                                # print(CNESerial)
                                try:
                                    CNERating = EquipmentRating[OrderData["NCM"][5:8]]
                                except:
                                    CNERating = "NA"
                           
                                COESerial = OrderData["OCM"]
                                # print(COESerial)
                                try:
                                    COERating = EquipmentRating[OrderData["OCM"][5:8]]
                                except:
                                    COERating = "NA"
                                CMSql="""
                                           UPDATE 
                                               [HES].[dbo].[SAI_NCRs]  
                                           SET  
                                               [RectificationDate] = '""" + OrderData['CompletionDate'] + """',  
                                               [RectifiedBy] = '""" + OrderData['WNO'] + """' , 
                                               [Status] = 7, 
                                               [NESerial] = '""" + CNESerial + """' ,  
                                               [NERating] = '""" + CNERating + """' ,
                                               [OESerial] = '""" + COESerial + """' ,  
                                               [OERating] = '""" + COERating + """' 
                                           where 
                                               NCRNumber = '""" + NCR_Number +"""_COM'"""
                                SQLs.append(CMSql)
                                # print(CMSql)
                  
          
                        if "ECBRep" in OrderData:
                            if OrderData["ECBRep"] in ['Y','y']:
                                ENESerial = OrderData["NECB"]
                                try:
                                    ECBNERating = EquipmentRating[OrderData["NECB"][5:8]]
                                except:
                                    ECBNERating = "NA"
                           
                                EOESerial = OrderData["OECB"]
                                try:
                                    EOERating = EquipmentRating[OrderData["OECB"][5:8]]
                                except:
                                    EOERating = "NA"
                                ECBSql="""
                                           UPDATE 
                                               [HES].[dbo].[SAI_NCRs]  
                                           SET  
                                               [RectificationDate] = '""" + OrderData['CompletionDate'] + """',  
                                               [RectifiedBy] = '""" + OrderData['WNO'] + """' , 
                                               [Status] = 7, 
                                               [NESerial] = '""" + ENESerial + """' ,  
                                               [NERating] = '""" + ECBNERating + """' ,
                                               [OESerial] = '""" + EOESerial + """' ,  
                                               [OERating] = '""" + EOERating + """' 
                                           where 
                                               NCRNumber = '""" + NCR_Number +"""_ECB'"""
                                SQLs.append(ECBSql)


                        
                    
                        #cr = clConn.cursor()
                        for SQL_St in SQLs:
                            # print(SQL_St)
                            re=0
                            while re>=0 and re<3:
                                try:
                                    cr.execute(SQL_St)
                                    re = -1
                                except:
                                    re += 1
                                    time.sleep(.5)
                            clConn.commit()
                    
                        print(Fore.GREEN + "Updated Order to Rectified: "+OrderData['NCRNumber'] +Style.RESET_ALL)

                        UpdateInboundMessage(MyMid,'100', "Order Complete")
                        # return{"Status":True, "Disc":"Order Complete"} 
                    
                # AddQ(OrderData,'Fail')
                # UpdateInboundMessage(MyMid,'20', "Missing key feilds")
                # return{"Status":False, "Disc":"Missing key feilds"} 
                
                
 
            ## CASE: CANCEL 
            #if OrderData['OrderStatus'] ==  80  and NCRstatus in [2,1] :
            #    if 'CancelReason' in OrderData and 'UId' in OrderData :
            #        # CancelDate = OrderData["CloseDate"]
            #        CancelBy = OrderData["UId"]
            #        CancelReason = OrderData["CancelReason"]
            #        UpdateSql = """ UPDATE [HES].[dbo].[SAI_NCRs] SET [Status] = 5 , [CancelDate] =getDate(),  [CancelReason] ='""" + CancelReason +"""',  [CancelBy] ='""" + CancelBy +"""' where NCRNumber = '""" + NCR_Number +"""'"""
            #        cr = clConn.cursor()
            #        cr.execute(UpdateSql)
            #        clConn.commit()
            #        return {'result': 'Order Canceled'}
            #    # AddQ(OrderData,'Fail')
            #    return {"result":"Missing key feilds"}
                
            # AddQ(OrderData,'Fail')
            UpdateInboundMessage(MyMid,'50', "Incorrect status request")
            # return{"Status":False, "Disc":"Incorrect status request"}
        UpdateInboundMessage(MyMid,'70', "NCR not created")
        # return{"Status":False, "Disc":"NCR not created"}
    UpdateInboundMessage(MyMid,'100', "updated orders")
    return{"Status":True, "Disc":"updated orders"}
   
       