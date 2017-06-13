import os
from lib.general import general
class archiver:
 def __init__(self,settings):
  self.settings=settings
  self.general=general(settings)
 def doArchive(self):
  cmdArr=[]
  z='7z a -mx9 -tzip '
  tf=self.settings.archiverTargetfile
  self.general.loggy('\nArchiving the generated data to '+tf+'...')
  cmdArr.append(z+tf+' '+self.settings.finalOutFolder)
  cmdArr.append(z+tf+' '+self.settings.datadirFlightradar)
  cmdArr.append(z+tf+' '+self.settings.finalJoinedDataCsv)
  cmdArr.append(z+tf+' '+self.settings.finalJoinedDataXlsx)
  cmdArr.append(z+tf+' '+self.settings.logfile)
  for cmd in cmdArr:
   self.general.loggy(cmd)
   try:
    os.system(cmd+' > /dev/null')
   except Exception as e:
    print(e)
    pass
