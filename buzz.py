import xmpp
from models import *

login = '<your primary user>'
pwd   = '<your primary user password>'

# Lets login
jid=xmpp.JID(login)
user, server = jid.getNode(), jid.getDomain()
cnx = xmpp.Client(server,debug=[])
conres = cnx.connect(server=('talk.google.com',5223))
authres = cnx.auth(user,pwd, 'Home')

def replier(conn,mess):
    text = mess.getBody()
    user = mess.getFrom().getStripped()
    user_obj = Users.get(email=user)[0] 
    if not text:
        return
    if text.startswith("*stop*"):
        params = text.split("*")
        if len(params)==1:
            users = Tracking.get(user_id=user_obj.id)
            for user in users:
                users.delete()
    elif text =="*pause*":
        user_obj.track=2
        user_obj.save()
    elif text =="*help*" or text=="help":
        cnx.send(xmpp.Message(user,"Please contact Dipankar (me@dipankar.name)"))
    elif text.startswith("***"):
        #This is from the feedparser code
        #***keyword id***Message
        params = text.split("***")
        users = Tracking.get(keyword_id=int(params[1]))
        for user in users:
            user_obj1 = Users.get(id=user.user_id)[0]
            if user_obj1.track==1:
                #print cnx.getRoster().getShow(user_obj1.email)
                cnx.send(xmpp.Message(user_obj1.email,params[2]))
    else: 
        #Registers the keyword
        kwd = Keyword.get(data=text)
        if kwd.count()==0:
            kwd = Keyword(data=text,updated_at=datetime.datetime.now())
            kwd.save()
        kwd = Keyword.get(data=text)[0]
        new_track = Tracking(users_id=user_obj.id,keyword_id=kwd.id)
        new_track.save()
    return

def adder(conn,presence):
    if presence:
        if presence.getType()=='subscribe':
             jid = presence.getFrom().getStripped()
             cnx.getRoster().Authorize(jid)
             new_user = Users(email=jid,track=1)
             new_user.save()
             cnx.send(xmpp.Message(presence.getFrom().getStripped(),"hello there, welcome to buzz tracker"))

cnx.RegisterHandler("presence", adder)
cnx.RegisterHandler("message", replier)
cnx.sendInitPresence()

while cnx.Process(1):
    pass

