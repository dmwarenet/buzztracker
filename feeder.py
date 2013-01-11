import xmpp
import feedparser
from models import *
import time,re
import urllib

login = '<Your feeder bot>'
pwd   = '<your feeder bot password>'

# Lets login
jid=xmpp.JID(login)
user, server = jid.getNode(), jid.getDomain()
cnx = xmpp.Client(server,debug=[])
conres = cnx.connect(server=('talk.google.com',5223))
authres = cnx.auth(user,pwd, 'Home')

def send_feed():
    kwds = Keyword.get()
    temp_url = "http://search.twitter.com/search.atom?q=%s"
    for k in kwds:
        feed_url = temp_url % (urllib.quote(k.data),)
        d = False
        try:
            d = feedparser.parse(feed_url)
        except UnicodeDecodeError,e:
            pass
        if d:
            fdate = k.updated_at
            entries = d.entries
            entries.reverse()
            for entry in entries:
                try:
                    dtuple = entry.updated_parsed
                    pdate = datetime.datetime(dtuple[0],dtuple[1],dtuple[2],dtuple[3],dtuple[4],dtuple[5])
                    fdate = pdate
                except AttributeError:
                    fdate = datetime.datetime.now()
                if pdate>k.updated_at:
                    content = entry.title
                    try:
                        content = entry.summary_detail.value
                    except AttributeError:
                        content = entry.content[0].value
                    content = re.sub('<([^!>]([^>]|\n)*)>', '', content)
                    cnx.send(xmpp.Message("<your primary>","***"+str(k.id)+"***"+content))
            k.updated_at = fdate
            k.save()

cnx.sendInitPresence()

while cnx.Process(1):
    send_feed()
    time.sleep(100)

