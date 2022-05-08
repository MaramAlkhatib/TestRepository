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