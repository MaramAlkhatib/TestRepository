import os
import win32com.client
def SendEmail(emailAddressesTo,emailAddressesCC ,emailAddressesBCC, subject, body, files):

 

    iConf = win32com.client.Dispatch("CDO.Configuration")
    Flds = iConf.Fields
    Flds("http://schemas.microsoft.com/cdo/configuration/smtpserver").Value = "outlook.alfanar.com"
    Flds("http://schemas.microsoft.com/cdo/configuration/smtpserverport").Value = 25
    Flds("http://schemas.microsoft.com/cdo/configuration/sendusing").Value = 2 # cdoSendUsingPort
    # Authentication and stuff
    Flds('http://schemas.microsoft.com/cdo/configuration/smtpauthenticate').Value = 1 # No authentication
    # The following fields are only used if the previous authentication value is set to 1 or 2
    # Flds('http://schemas.microsoft.com/cdo/configuration/smtpaccountname').Value = "user"
    Flds('http://schemas.microsoft.com/cdo/configuration/sendusername').Value = "ehab.maher@alfanar.com"
    # Flds('http://schemas.microsoft.com/cdo/configuration/sendpassword').Value = "password"
    Flds.Update()
    iMsg = win32com.client.Dispatch("CDO.Message")
    iMsg.Configuration = iConf
    iMsg.To = ";".join(emailAddressesTo)
    iMsg.CC = ";".join(emailAddressesCC)
    iMsg.BCC = ";".join(emailAddressesBCC)
    iMsg.From = "SMP_Robot<SMPRobot@alfanar.com>"
    iMsg.Subject = subject
    #iMsg.TextBody = body
    iMsg.HTMLBody = body
    # The following assumes the files to be in the current directory
    for file in files:
        #iMsg.AddAttachment("file:///" + "C:/Clevest/SEC_Status/" + file)
        print(file)
        iMsg.AddAttachment(file)
    return iMsg.Send()
#SendEmail(["Ehab.Maher@alfanar.com"],'Hi','Hi',["D:/HES2021/20210320210325.pdf"])