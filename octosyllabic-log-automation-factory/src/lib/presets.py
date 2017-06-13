import calendar,re
from datetime import datetime as dt
from datetime import timedelta as td
from lib.file_ops import fileOps
from lib.general import general
from lib.settings import settings
s=settings(None)
g=general(None)
class presets:
 def __init__(self):
  self.longTimeformat='%Y-%m-%d %H:%M:%S'
  self.shortTimeformat='%Y-%m-%d'
  self.readJson=fileOps.readJson
  self.commercialTailIdList=s.dataCommercialAcList
 def mkdate(self,datestr,diff=0):
  dateObj=dt.strptime(datestr+' 00:00:00',self.longTimeformat)
  if diff!=0:
   dateObj=dateObj-td(days=diff)
  dic={}
  dic['dateobj']=dateObj
  dic['posix']=calendar.timegm(dateObj.timetuple())
  dic['string']=dt.strftime(dateObj,self.shortTimeformat)
  return(dic)
 def makeDateStringPosix(self,datestr):
  dateObj=dt.strptime(datestr+' 00:00:00',self.longTimeformat)
  return(calendar.timegm(dateObj.timetuple()))
 def getDateString(self,dtype,diff=0):
  if dtype=='end':
   diff-=1
  ds=dt.utcnow()
  dateString=dt.strftime(ds,self.shortTimeformat)
  return(self.mkdate(dateString,diff))
 def checkRegexScheme(self,val):
  try:
   re.compile(val)
  except Exception as e:
   raise ValueError('No valid regex scheme.')
  else:
   return(val)
 def calculateDataSyncTimespan(self,startTimeObj):
  d=str(dt.utcnow()-startTimeObj)
  d=d.split(' ')[0]
  return(int(d))
