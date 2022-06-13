
from glob import glob
import pandas as pd
import pyodbc

SECMDHere = pd.DataFrame()

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.90.10.173,21532;DATABASE=Clevest;UID=Clevest;PWD=!C13ve$T')

def GetFromSEC(Key, Criteria):
    global SECMDHere
    print(SECMDHere)
    print(SECMDHere.columns)
    OData = pd.DataFrame()
    #Meter Number
    if Key == 'MSN':
        OData = SECMDHere[SECMDHere['fg. Ser. No']==Criteria]
        
    #Premise
    elif Key == 'PRE':
        OData = SECMDHere[SECMDHere['Premise']==str(Criteria)]
        print(OData)      
        print("_________________________________________________________________________________")      

    #Subscription
    elif Key == 'SBS':
        OData = SECMDHere[SECMDHere['Subscription No']==str(Criteria)]        
    #Account Number
    elif Key == 'ACN':
        OData = SECMDHere[SECMDHere['Account No']==str(Criteria)]
    return OData



def GetMeterTech(MSN):
    try:
        if (MSN[0:3] == "KFM" and ( MSN[7:10] in ('866','766') or MSN[3:9] == '212076' or (int(MSN[3:]) >= 2020760240903 and int(MSN[3:]) <= 2020760241119))) or (MSN[0:3] == "AES" and MSN[7:10] == '896') or (MSN[0:3] == "SMR" and MSN[7:10] == '856'):
            return "PLC"
        else:
            return "NB-IoT"
    except:
            return "N.A."

def GetMeterRating(MSN, MType):
    try:    
        MeterRatings = {
                "208" : "WC100A",
                "207" : "WC160A",
                "201" : "Digital SEC Legacy Meter",
                "203" : "Digital SEC Legacy Meter",
                "204" : "Digital SEC Legacy Meter",
                "205" : "CT-VT Meter",
                "206" : "CT Meter",
        }
        return MeterRatings[MSN[5:8]] + " / " + MType
    except:
        return "N.A."



def GetMeterData(Key, Criteria):
    OData = GetFromSEC(Key, Criteria)
    # print(OData.iloc[0]['SignalStrength'])      

    if len(OData) > 0:
        Region = ""
        if OData.iloc[0]['Office'][0:1] == "3":
            Region = "Eastern"
        else:
            Region = "Central"
        GetMeterRating(OData.iloc[0]['fg. Ser. No'], OData.iloc[0]['Meter Type'] )
        
        # print(OData.iloc[0]['MeterList'])      
        # print(OData.iloc[0]['DCUSerialNumber'])     
        if OData.iloc[0]['Meter Type'] == "DCU": 
            return {
            "data":{
                    "Premise" : OData.iloc[0]['Premise'],
                    "SubScriptionNum" : OData.iloc[0]['Subscription No'],
                    "MeterSN" : OData.iloc[0]['fg. Ser. No'],
                    "Longitude" : OData.iloc[0]['Longitude'],
                    "Latitude" : OData.iloc[0]['Latitude'],
                    "AccountNumber" : OData.iloc[0]['Account No'],
                    "Office" : OData.iloc[0]['Office'],
                    "Region" : Region,
                    "MeterType" : OData.iloc[0]['Meter Type'],
                    # "MeterType" : GetMeterRating(OData.iloc[0]['fg. Ser. No'], OData.iloc[0]['Meter Type'] ) if len(OData.iloc[0]['Premise'].split('-')) < 3 else "DCU Device",
                    "Technology" : GetMeterTech(OData.iloc[0]['fg. Ser. No']),
                    "TarifType" :OData.iloc[0]['Tariff Type'],
                    "PreReading" : OData.iloc[0]['Prev. Read T'],
                    "PreReadDate" : OData.iloc[0]['Prev Read Date T'],
                    "BreakerCapacity" : OData.iloc[0]['Breaker Cap.'],
                    "MRU" : OData.iloc[0]['MRU'],
                    "EquipNum" : OData.iloc[0]['Equip. No'],
                    "RoutSeq" : OData.iloc[0]['Route Read Seq'],
                    "LastBill" : OData.iloc[0]['Last Bill Key'],
                    "BreakerSN" : "",
                    "CommModule" : "",
                    "MeterList" : OData.iloc[0]['MeterList'],
                    # "SignalStrength" : OData.iloc[0]['SignalStrength'],
                    "DCUSerialNumber" : OData.iloc[0]['DCUSerialNumber'],
                    "TransformerID" : OData.iloc[0]['TransformerID'],
                    "TransformerRating" : OData.iloc[0]['TransformerRating'],
                    "PowerConnected" : OData.iloc[0]['PowerConnected'],
                    "PowerConnectionDate" : OData.iloc[0]['PowerConnectionDate'],
                    "PowerStatusUpdatedBy" : OData.iloc[0]['PowerStatusUpdatedBy'],
                    "CTavailable" : OData.iloc[0]['CTavailable'],
                    "CTConnected" : OData.iloc[0]['CTConnected'],
                    "CTRatio" : OData.iloc[0]['CTRatio'],
                    }
        }
        else:
            return {
            "data":{
                    "Premise" : OData.iloc[0]['Premise'],
                    "SubScriptionNum" : OData.iloc[0]['Subscription No'],
                    "MeterSN" : OData.iloc[0]['fg. Ser. No'],
                    "Longitude" : OData.iloc[0]['Longitude'],
                    "Latitude" : OData.iloc[0]['Latitude'],
                    "AccountNumber" : OData.iloc[0]['Account No'],
                    "Office" : OData.iloc[0]['Office'],
                    "Region" : Region,
                    "MeterType" : GetMeterRating(OData.iloc[0]['fg. Ser. No'], OData.iloc[0]['Meter Type'] ) ,
                    "Technology" : GetMeterTech(OData.iloc[0]['fg. Ser. No']),
                    "TarifType" :OData.iloc[0]['Tariff Type'],
                    "PreReading" : OData.iloc[0]['Prev. Read T'],
                    "PreReadDate" : OData.iloc[0]['Prev Read Date T'],
                    "BreakerCapacity" : OData.iloc[0]['Breaker Cap.'],
                    "MRU" : OData.iloc[0]['MRU'],
                    "EquipNum" : OData.iloc[0]['Equip. No'],
                    "RoutSeq" : OData.iloc[0]['Route Read Seq'],
                    "LastBill" : OData.iloc[0]['Last Bill Key'],
                    "BreakerSN" : "",
                    "CommModule" : ""
                    }
        }
    else:
        return {}

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#--------------------------------Search In Clevest Data------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def GetFromClevest(Key, Criteria):
    SQLCriteria = ""
    OData = pd.DataFrame()
    if Key == 'MSN':
        SQLCriteria = "Mex_NewMeterNumber = '" + str(Criteria) + "'"
    #Premise
    elif Key == 'PRE':
        SQLCriteria = "WOM.HostOrderNumber = '" + str(Criteria) + "'"
    #Subscription
    elif Key == 'SBS':
        SQLCriteria = "FH_SubscriptionNumber = '" + str(Criteria) + "'"      
    #Account Number
    elif Key == 'ACN':
        SQLCriteria = "FH_ContractAccount = '" + str(Criteria) + "'"  
    if len(SQLCriteria) > 0:
        SQLStr = """ select top(1)
	                    WOM.HostOrderNumber, FH_SubscriptionNumber, 
	                    MEX_NewMeterNumber, Longitude, Latitude, 
	                    FH_ContractAccount ,FH_OfficeCode, 
	                    iif(FH_officeCode > 2000, 'Eastern', 'Central') as Region,
	                    MEX_NewMeterType, MEX_NewMeterRating, SMOC_Communication, 
	                    RD_TariffType, MEX_BreakerCapacity, MEX_NewBreakerNumber, MEX_CommunicationModule
                    from 
                        WorkOrderMapping WOM inner join WorkOrder WO on WO.Id = WOM.Id
                    where 
                        wom.OrderStatusId in (100,50) and 
                        """ + SQLCriteria
        print(SQLStr)
    else:
        SQLStr = """ select top(1)
	                    WOM.HostOrderNumber, FH_SubscriptionNumber, 
	                    MEX_NewMeterNumber, Longitude, Latitude, 
	                    FH_ContractAccount ,FH_OfficeCode, 
	                    iif(FH_officeCode > 2000, 'Eastern', 'Central') as Region,
	                    MEX_NewMeterType, MEX_NewMeterRating, SMOC_Communication, 
	                    RD_TariffType, MEX_BreakerCapacity, MEX_NewBreakerNumber, MEX_CommunicationModule
                    from 
                        WorkOrderMapping WOM inner join WorkOrder WO on WO.Id = WOM.Id
                    where 
                        wom.OrderStatusId in (1200) 
                        """

    OData = pd.read_sql(SQLStr, conn)
    return OData.fillna("NA")

def GetMeterDataCL(Key, Criteria):
    OData = GetFromClevest(Key, Criteria)
    print(OData)
    if len(OData) > 0:
        return {
            "data":{
                    "Premise" : str(OData.iloc[0]['HostOrderNumber']),
                    "SubScriptionNum" : str(OData.iloc[0]['FH_SubscriptionNumber']),
                    "MeterSN" : OData.iloc[0]['MEX_NewMeterNumber'],
                    "Longitude" : str(OData.iloc[0]['Longitude']),
                    "Latitude" : str(OData.iloc[0]['Latitude']),
                    "AccountNumber" : OData.iloc[0]['FH_ContractAccount'],
                    "Office" : str(OData.iloc[0]['FH_OfficeCode']),
                    "Region" : OData.iloc[0]['Region'],
                    "MeterType" : OData.iloc[0]['MEX_NewMeterType'] + " / " + OData.iloc[0]['MEX_NewMeterRating'],
                    "Technology" : OData.iloc[0]['SMOC_Communication'],
                    "TarifType" : OData.iloc[0]['RD_TariffType'],
                    "PreReading" : "",
                    "PreReadDate" : "",
                    "BreakerCapacity" : str(OData.iloc[0]['MEX_BreakerCapacity']),
                    "MRU" : "",
                    "EquipNum" : "",
                    "RoutSeq" : "",
                    "LastBill" : "",
                    "BreakerSN" : OData.iloc[0]['MEX_NewBreakerNumber'],
                    "CommModule" : OData.iloc[0]['MEX_CommunicationModule']
                    }
        }
    else:
        return {}