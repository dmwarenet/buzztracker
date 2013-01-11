from autumn.db.connection import autumn_db
from autumn.model import Model
from autumn.db.relations import ForeignKey, OneToMany
import datetime

autumn_db.conn.connect('postgres', user='root', db='buzztracker')

class Users(Model):
    class Meta:
        pass

class Keyword(Model):
    class Meta:
        pass
    
class Tracking(Model):
    keyword = ForeignKey(Keyword)
    users = ForeignKey(Users)
    class Meta:
        pass

