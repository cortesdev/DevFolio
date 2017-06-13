import csv,json,os,re
from subprocess import Popen,PIPE,STDOUT
class fileOps:
 def findFiles(folder,rxFilter=r'.*',fullname=False,recursive=False):
  foundFolders=[folder]
  foundFiles=[]
  if recursive is True:
   for root,directories,filenames in os.walk(folder):
    for directory in directories:
     foundFolders.append(os.path.join(root,directory))
  for f in foundFolders:
   for file in os.listdir(f):
    if os.path.isfile(os.path.join(f,file)):
     if bool(re.search(rxFilter,file))is True:
      if fullname is True:
       foundFiles.append(f+'/'+file)
      else:
       foundFiles.append(file)
  return(sorted(foundFiles))
 def readFile(filename):
  arr=[]
  filecontent=open(filename,'r')
  for line in filecontent.read().splitlines():
   if line and line.startswith('#')is False:
    arr.append(line)
  return(arr)
 def runCmd(cmd,comment=None,debug=False):
  if comment is not None:
   print('\n'+comment)
  if debug is True:
   print(cmd)
  p=Popen(cmd,stdin=PIPE,stdout=PIPE,stderr=STDOUT,close_fds=True,shell=True)
  out,err=p.communicate()
  if debug is True:
   print(out.decode('utf-8'))
  return(out.decode('utf-8'))
 def runCmdSimple(cmd,comment=None,debug=False):
  if comment is not None:
   print('\n'+comment)
  if debug is True:
   print(cmd)
  else:
   os.system(cmd)
 def readJson(filename):
  with open(filename)as json_data:
   d=json.load(json_data)
   return(d)
 def writeJson(filename,data):
  with open(filename,'w')as outfile:
   json.dump(data,outfile,indent=4,sort_keys=True)
 def writeCsv(filename,dataArray):
  print('\nWriting final csv output file...')
  outputFile=open(filename,'w',newline='')
  outputWriter=csv.writer(outputFile,delimiter=';',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
  for d in dataArray:
   outputWriter.writerow(d)
  outputFile.close()
