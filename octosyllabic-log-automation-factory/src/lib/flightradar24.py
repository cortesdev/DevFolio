import datetime,requests
from lib.file_ops import fileOps as fo
from lib.general import general
from lib.log_parsers import logParsers
from lib.presets import presets
token=''
class flightradar24:
 def __init__(self,settings):
  self.settings=settings
  self.args=settings.args
  self.lpa=logParsers(settings)
  self.general=general(settings)
  self.pre=presets()
  self.posix2000=946684800
 def getFlighttime(self,jsonData):
  def getTime(flightstate,jsonDate):
   timeTypes=['real','estimated','scheduled','other']
   for timeType in timeTypes:
    r=None
    try:
     r=int(jsonDate['time'][timeType][flightstate])
     if r<self.posix2000:
      raise ValueError('This does not seem to be a valid unix timestamp.')
    except Exception as e:
     r=None
     pass
    else:
     break
   if r is None:
    return(0,'unknown')
   else:
    return([r,timeType])
  flighttime={}
  departure_uts=getTime('departure',jsonData)
  departure_date=self.unixTimestampToDate(departure_uts,-1800)
  flighttime['departure']=departure_date
  arrival_uts=getTime('arrival',jsonData)
  arrival_date=self.unixTimestampToDate(arrival_uts,900)
  flighttime['arrival']=arrival_date
  return(flighttime)
 def getJsonData(self,url):
  headers=requests.utils.default_headers()
  headers.update({'Host':'api.flightradar24.com','User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'de,en-US;q=0.7,en;q=0.3','Accept-Encoding':'gzip, deflate, br'})
  r=requests.get(url,headers=headers)
  r=r.json()
  return(r)
 def getTailHistory(self,tailNo,c=0):
  if c<4:
   url='https://api.flightradar24.com/common/v1/flight/list.json?query='+tailNo+'&fetchBy=reg&page=1&limit=100' 
   try:
    c+=1
    json=self.getJsonData(url)
    json=json['result']['response']['data']
   except Exception as e:
    self.getTailHistory(tailNo,c)
   else:
    return(json)
  else:
   return(None)
 def unixTimestampToDate(self,unixTimestamp,diff):
  dateObj={}
  try:
   dateObj['timestamp']=datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%Y%m%d%H%M%S')
   dateObj['date']=datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%Y%m%d')
   dateObj['day']=int(datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%d'))
   dateObj['month']=int(datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%m'))
   dateObj['year']=int(datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%Y'))
   dateObj['week_of_year']=int(datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%V'))
   dateObj['time']=datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%H%M%S')
   dateObj['hour']=int(datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%H'))
   dateObj['minute']=int(datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%M'))
   dateObj['second']=int(datetime.datetime.utcfromtimestamp(unixTimestamp[0]).strftime('%S'))
   dateObj['userdata_collection_time']=datetime.datetime.utcfromtimestamp(unixTimestamp[0]+diff).strftime('%Y-%m-%d %H:%M:%S')
   dateObj['userdata_collection_timestamp']=int(datetime.datetime.utcfromtimestamp(unixTimestamp[0]+diff).strftime('%Y%m%d%H%M%S'))
   dateObj['posix']=unixTimestamp[0]
   dateObj['time_type']=unixTimestamp[1]
  except Exception as e:
   pass
  return(dateObj)
 def lookForNewFlights(self,tailId):
  existingDataFile=self.settings.datadirFlightradar+tailId.lower()+'.json'
  try:
   existingData=fo.readJson(existingDataFile)
   self.general.loggy('Found '+str(len(existingData))+' flights for '+tailId+'.')
  except Exception as e:
   self.general.loggy(e)
   existingData={}
   pass
  responseData=self.getTailHistory(tailId)
  if responseData is not None:
   for d in responseData:
    tailId=d['aircraft']['registration']
    flightNo=d['identification']['callsign']
    flighttime=self.getFlighttime(d)
    departure=flighttime['departure']['date']
    uuid=str(tailId).lower()+'_'+str(flightNo).lower()+'_'+str(departure).lower()
    if self.lpa.checkUuidSyntax(uuid)is True:
     existingData[uuid]=d
   fo.writeJson(existingDataFile,existingData)
  return(responseData)
 def requestFr24Flights(self):
  self.general.loggy('\nNow requesting data from flightradar24...')
  for ac in self.settings.dataCommercialAcList:
   self.general.loggy('Getting historic data of tail id: '+ac+'...')
   if self.args.debug is False:
    self.lookForNewFlights(ac.lower())
    self.general.countdown(10)
 def makePosixFromJsonAtom(self,dateString):
  posix=str(dateString)[0:4]+'-'+str(dateString)[4:6]+'-'+str(dateString)[6:8]
  posix=self.pre.makeDateStringPosix(posix)
  return(posix)
 def syncAndParseFlightradar(self):
  self.general.loggy('Will apply the following settings when filtering flights. Filtering by posix.')
  self.general.loggy('Collection start time: '+str(self.settings.args.start_time))
  self.general.loggy('Collection end time: '+str(self.settings.args.end_time))
  start=self.settings.args.start_time['posix']
  end=self.settings.args.end_time['posix']
  self.requestFr24Flights()
  returnData={'dataset_id':'flightradar'}
  self.general.loggy('\nProcessing flightradar data...')
  for ac in self.settings.dataCommercialAcList:
   startDate=self.makePosixFromJsonAtom(self.settings.dataCommercialAcList[ac]['startdate'])
   try:
    commercialSince=self.makePosixFromJsonAtom(self.settings.dataCommercialAcList[ac]['commercial'])
   except Exception as e:
    commercialSince=self.makePosixFromJsonAtom('20360207')
   frDataFile=self.settings.datadirFlightradar+ac.lower()+'.json'
   jsonTailId=fo.readJson(frDataFile)
   self.general.loggy('Now at tail id '+ac+' which has '+str(len(jsonTailId))+' flights in db...')
   for e in jsonTailId:
    dataset=jsonTailId[e]
    flighttime=self.getFlighttime(dataset)
    try:
     flightNo=dataset['identification']['callsign']
     flightNo=flightNo.lower()
    except Exception as e:
     pass
    try:
     tailId=dataset['aircraft']['registration']
     tailId=tailId.lower()
    except Exception as e:
     pass
    try:
     ts=flighttime['departure']['date']
    except Exception as e:
     ts=str(999999999999)
    uuid=str(tailId)+'_'+str(flightNo)+'_'+ts
    try:
     ps=flighttime['departure']['posix']
    except Exception as e:
     ps=str(999999999999)
    reportString='[S:'+str(start)+', F:'+str(ps)+', E:'+str(end)+' / S:'+str(startDate)+', C:'+str(commercialSince)+']'
    if(int(start)<=int(ps)and int(ps)<=end)and int(ps)>startDate:
     logString='Flight '+uuid+' did match filter. Will be reported. '+reportString
     returnData[uuid]={}
     returnData[uuid]['arrival']=flighttime['arrival']
     returnData[uuid]['departure']=flighttime['departure']
     returnData[uuid]['identification']=dataset['identification']
     returnData[uuid]['flight_no']=dataset['identification']['callsign']
     returnData[uuid]['aircraft']=dataset['aircraft']
     returnData[uuid]['airport']=dataset['airport']
     if commercialSince<ps:
      logString+=' (commercial flight)'
      returnData[uuid]['commercial_flight']=True
     else:
      returnData[uuid]['commercial_flight']=False
      logString+=' (not a commercial flight)'
     returnData[uuid]['flight_duration']=self.posixTimedelta(flighttime['departure']['posix'],flighttime['arrival']['posix'])
    else:
     logString='Flight '+uuid+' did not match the date filter. '+reportString
    self.general.loggy(logString)
  self.general.loggy('Writing flightradar.json and returning the dataset...')
  fo.writeJson(self.settings.finalFlightradarJson,returnData)
 def posixTimedelta(self,start,end):
  if start<self.posix2000 or end<self.posix2000:
   return('-')
  else:
   arr=[start,end]
   arr=sorted(arr)
   duration=arr[1]-arr[0]
   duration=str(datetime.timedelta(seconds=duration))
   return(duration)
