from lib.file_ops import fileOps as fo
from mailjet_rest import Client
from lib.general import general
import base64,datetime,re
class mailjet:
 def __init__(self,settings):
  self.settings=settings
  self.args=settings.args
  self.api_key='630b87632095f373d3930b5a71fbead6'
  self.api_secret='08b805355878ed6e345a6392f7b31a04'
  self.recipients=fo.readJson(self.settings.mailjetRecipients)
  self.general=general(settings)
 def fileToBase64(self,filename):
  with open(filename,'rb')as image_file:
   r=base64.b64encode(image_file.read())
   r=r.decode('utf-8')
  return(r)
 def createAttachment(self,filename,contentType):
  attachment={}
  attachment['Content-type']=contentType
  rfn=re.search(r'(.*\/)(.*)',filename).group(2)
  attachment['Filename']=rfn
  attachment['content']=self.fileToBase64(filename)
  return(attachment)
 def parseRecipientsList(self):
  self.general.loggy('Gathering recipients to send mails to...')
  recipientsSimple={}
  recipientsPlusZip={}
  rSim=[]
  rPlus=[]
  for r in self.recipients:
   if r['mailtype']=='simple' and r['enabled']is True:
    rSim.append(r)
   elif r['mailtype']=='pluszip' and r['enabled']is True:
    rPlus.append(r)
  if len(rSim)>0:
   recipientsSimple['recipients']=rSim
   att=[]
   att.append(self.createAttachment(self.settings.finalJoinedDataCsv,'application/csv'))
   att.append(self.createAttachment(self.settings.finalJoinedDataXlsx,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
   recipientsSimple['attachment']=att
  if len(rPlus)>0:
   recipientsPlusZip['recipients']=rPlus
   att=[]
   att.append(self.createAttachment(self.settings.finalJoinedDataCsv,'application/csv'))
   att.append(self.createAttachment(self.settings.finalJoinedDataXlsx,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
   att.append(self.createAttachment(self.settings.archiverTargetfile,'application/x-7z-compressed'))
   recipientsPlusZip['attachment']=att
  return([recipientsSimple,recipientsPlusZip])
 def generateTimedeltaText(self):
  text=''
  endTime=datetime.datetime.now()
  timedelta=endTime-self.settings.startTime
  timedelta=str(timedelta).split('.')[0]
  timedelta=str(timedelta).split(':')
  tdh=int(timedelta[0])
  tdm=int(timedelta[1])
  tds=int(timedelta[2])
  if tdh==1:
   text=' an hour'
  elif tdh>1:
   text=' '+str(tdh)+' hours'
  if tdm==1:
   text+=' '+str(tdm)+' minute'
  elif tdm>1:
   text+=' '+str(tdm)+' minutes'
  if len(text)>5:
   text+=' and'
  if tds==1:
   text+=' '+str(tds)+' second'
  elif tds>1:
   text+=' '+str(tds)+' seconds'
  if len(text)<1:
   text=' no time'
  return(text)
 def sendReport(self):
  recipients=self.parseRecipientsList()
  self.general.loggy('\nMail reports go out into the world...')
  mailjet=Client(auth=(self.api_key,self.api_secret))
  for r in recipients:
   try:
    r['recipients']
   except Exception as e:
    self.general.loggy(e)
    pass
   else:
    mailtext='<p>Attached you will find an automatically generated report. It contains data between today and '+ str(self.settings.args.timespan_data_collection)+' days back.</p>'+ '<p>Generating these splendidly dazzling and well-formed statistics took me'+self.generateTimedeltaText()+'.'+ '<p>Please mail comments and feedback to <a href="mailto:olaf@paxlife.aero">olaf@paxlife.aero</a>.</p>'+ '<p>Have fun.</p>'
    self.general.loggy('Sending to: '+str(r['recipients']))
    self.general.loggy('Mailtext: '+mailtext)
    data={'FromEmail':'reports@cloud10.net','FromName':'Cloud 10 Automatic Reports','Subject':'Commercial Aircraft Log Report','Text-part':'Attached you will find an automatically generated report.','Html-part':mailtext,'Recipients':r['recipients'],'Attachments':r['attachment']}
    if self.args.sendmail is True:
     response=mailjet.send.create(data=data)
     self.general.loggy(response.status_code)
     self.general.loggy(response.json())
