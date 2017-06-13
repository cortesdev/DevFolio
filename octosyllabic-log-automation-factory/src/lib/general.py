import json,os,re,sys,time
from lib.settings import settings
s=settings(None)
class general:
 def __init__(self,settings):
  self.settings=settings
  self.pid=str(os.getpid())
  self.pidfile='/tmp/olaf.pid'
  self.commercialTailIdList=s.dataCommercialAcList
 def countdown(self,timer):
  print('')
  for i in range(0,timer+1):
   time.sleep(1)
   t=timer-i
   self.lineUpAndClear()
   print('Waiting for '+str(t)+' seconds...')
 def deletePid(self):
  try:
   os.remove(self.pidfile)
  except Exception as e:
   pass
 def dropPid(self):
  if os.path.isfile(self.pidfile):
   os.system('clear')
   print('\nOLAF is already running. You should wait till it is finished...\n')
   sys.exit()
  f=open(self.pidfile,'w')
  f.write(self.pid)
  f.close()
 def digger(self,baseString,length,filler):
  baseString=str(baseString)
  filler=str(filler)
  while len(baseString)<length:
   baseString=filler+baseString
  return(baseString)
 def filterTailIdList(self,filterString,filtertype):
  r={}
  if filtertype=='regex':
   fs=re.compile(filterString,re.IGNORECASE)
   for tid in self.commercialTailIdList:
    if bool(re.search(fs,tid)):
     r[tid]=self.commercialTailIdList[tid]
  else:
   for tid in self.commercialTailIdList:
    if tid.lower()==filterString.lower():
     r[tid]=self.commercialTailIdList[tid]
  return(r)
 def lineUpAndClear(self):
  sys.stdout.write('\033[F')
  sys.stdout.write('\033[2K')
 def loggy(self,message,silent=False):
  timestamp=self.settings.getTimestamp(' ')
  message=str(message)
  if silent is False:
   print(message)
  message=message.replace('\n','')
  with open(self.settings.logfile,'a')as myfile:
   myfile.write('['+timestamp+'] '+message+'\n')
 def printJson(self,jsonData):
  print(json.dumps(jsonData,sort_keys=True,indent=4))
 def queryOnFilterResults(self,dic):
  print('\nFilter applied. The following tail id information will be processed...\n')
  self.printJson(dic)
  if self.settings.args.yes is False:
   i=input('\nDo you want to continue?  y/n   ')
   if i.lower()!='y':
    print('\nYou did not approve. Ending here.\n')
    sys.exit()
 def waitOnKey(self):
  print('\nPress key to continue...\n')
  input('')
