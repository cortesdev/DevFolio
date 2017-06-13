import os,re
from lib.file_ops import fileOps as fo
from lib.general import general
class logsToLocal:
 def __init__(self,settings):
  self.settings=settings
  self.general=general(settings)
 def doExtractFile(self,archive,targetfolder,filetype):
  os.system('mkdir -p '+targetfolder)
  if filetype=='gz' or filetype=='zip' or filetype=='tar':
   cmd='7z x "'+archive+'" -o"'+targetfolder+'" -pX -y'
  else:
   cmd='echo "Unknown filetype. Taking no action."'
  self.general.loggy('Extracting file '+archive+'...')
  if self.settings.args.debug is False:
   r=fo.runCmd(cmd)
   if 'cannot' in r:
    os.system('mkdir -p '+self.settings.datadirLocalTmpCorrupted)
    os.system('mv '+archive+' '+self.settings.datadirLocalTmpCorrupted+'/'+archive.replace('/','_'))
   else:
    os.system('rm '+archive)
  else:
   self.general.loggy(cmd)
 def doSyncToLocal(self):
  os.system('mkdir -p '+self.settings.datadirLocalLogfiles)
  for folder in self.settings.datadirRemoteArr:
   cmd=self.settings.rsyncBase+' "'+self.settings.datadirRemoteBase+folder+'" "'+self.settings.datadirLocalLogfiles+folder+'"'
   self.general.loggy('\nSyncing remote data to local...')
   if self.settings.args.debug is False:
    self.general.loggy(cmd)
    os.system(cmd)
   else:
    self.general.loggy(cmd)
 def doSyncToTemp(self):
  os.system('mkdir -p '+self.settings.datadirLocalTmpExtracted)
  cmdFind='find "'+self.settings.datadirLocalLogfiles+'" -type f -mtime -'+str(self.settings.args.timespan_file_sync)
  xclTemp=fo.runCmd(cmdFind).splitlines()
  xclList=[]
  for f in xclTemp:
   xclList.append(f.replace(self.settings.datadirLocalLogfiles,''))
  exclTemp='/tmp/rsync-exclude.txt'
  f=open(exclTemp,'w')
  xclList=sorted(xclList)
  for item in xclList:
   f.write(item+'\n')
  f.close()
  cmd='rsync -av --files-from='+exclTemp+' "'+self.settings.datadirLocalLogfiles+'" "'+self.settings.datadirLocalTmpExtracted+'"'
  if self.settings.args.debug is False:
   os.system('rm -rf "'+self.settings.datadirLocalTmpExtracted+'"')
   os.system('mkdir -p "'+self.settings.datadirLocalTmpExtracted+'"')
   self.general.loggy('\nSyncing from local to temp...')
   os.system(cmd)
  else:
   self.general.loggy(cmd)
 def doExtractFoundFiles(self,rx,filetype):
  self.general.loggy('\nExtracting '+filetype+' files in temp folder...')
  while bool(fo.findFiles(self.settings.datadirLocalTmpExtracted,rx,True,True))is True:
   for archive in fo.findFiles(self.settings.datadirLocalTmpExtracted,rx,True,True):
    targetfolder=re.search(r'.*\/',archive).group(0)
    self.doExtractFile(archive,targetfolder,filetype)
 def extractAll(self):
  os.system('chmod -R 777 '+self.settings.datadirLocalTmpExtracted)
  rxZip=r'^(?!.*(prestashop\.zip$|revive\.zip$)).*\.zip$'
  self.doExtractFoundFiles(rxZip,'zip')
  self.doExtractFoundFiles(r'.*\.gz$','gz')
