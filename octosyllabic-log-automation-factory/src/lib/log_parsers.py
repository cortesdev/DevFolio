from lib.aggregators import aggregators
from lib.file_ops import fileOps as fo
from lib.general import general
import json,re
class logParsers:
 def __init__(self,settings):
  self.settings=settings
  self.aggregators=aggregators(self.settings)
  self.general=general(self.settings)
 def checkUuidSyntax(self,uuid):
  self.general.loggy('\nChecking syntax of '+uuid+'...')
  r=bool(re.search(self.settings.rxValidUuid,uuid))
  self.general.loggy('Result is '+str(r)+'.')
  return(r)
 def createDateObj(self,timestamp):
  dic={}
  dic['timestamp']=int(timestamp)
  try:
   dic['day']=timestamp[6:8]
   dic['month']=timestamp[4:6]
   dic['year']=timestamp[0:4]
   dic['hour']=timestamp[8:10]
   dic['minute']=timestamp[10:12]
   dic['second']=timestamp[-2:]
   dic['date']=int(timestamp[0:8])
   dic['time']=int(timestamp[8:])
  except Exception as e:
   pass
  return(dic)
 def filterArray(self,arr,regex,group=0):
  result=[]
  rx=re.compile(regex,re.IGNORECASE)
  for a in arr:
   match=re.search(rx,a)
   if bool(match)is True:
    result.append(match.group(group))
  if len(result)==0:
   result=None
  elif len(result)==1:
   result=result[0]
  return(result)
 def parseCsv(self,filename,sep=','):
  content=fo.readFile(filename)
  header=content[0].split(sep)
  data=content[1].split(sep)
  line={}
  for i,h in enumerate(header):
   try:
    line[h.lower()]=int(data[i])
   except Exception as e:
    line[h.lower()]=data[i]
  return(line)
 def parseOverallStats(self):
  overallStats={'dataset_id':'overall'}
  files=fo.findFiles(self.settings.tmpdir,r'overall_stat\.csv$',True,True)
  for f in files:
   relevantPart=re.search(r'(?<=media4sky\/).*(?=\/overall_stat\.csv)',f).group(0)
   date=re.search(r'(?<=_).*?(?=_)',relevantPart).group(0)
   time=re.search(r'([^_]*)$',relevantPart).group(0)
   tailId=re.search(r'.*?(?=\/)',relevantPart).group(0)
   flightNo=re.search(r'(?<=\/).*?(?=_)',relevantPart).group(0)
   line={}
   line['tail_id']=tailId
   line['flightnr']=flightNo
   line['filename']=f
   line['logdate']=self.createDateObj(date+time)
   line['overall_stats']=self.parseCsv(f)
   try:
    uuid=tailId.lower()+self.settings.uuidDelimiter+flightNo.lower()+self.settings.uuidDelimiter+str(line['overall_stats']['date'])
   except Exception as e:
    uuid=tailId.lower()+self.settings.uuidDelimiter+flightNo.lower()+self.settings.uuidDelimiter+date
   overallStats[uuid]=line
  self.general.loggy('Writing '+self.settings.finalOverallJson+'...')
  fo.writeJson(self.settings.finalOverallJson,overallStats)
 def parseAvionicLogs(self):
  self.general.loggy('\nParsing avionic logs...')
  avionicLogData={}
  files=fo.findFiles(self.settings.tmpdir,r'avionic.*\.(log|log[-0-9]*)$',True,True)
  for f in files:
   self.general.loggy('Now at file '+f)
   try:
    relevantPart=re.search(r'(?<=avionic\/).*(?=\.log)',f).group(0)
   except Exception as e:
    pass
   else:
    content=fo.runCmd('grep -i wap_status "'+f+'"').splitlines()
    wap_events=self.filterArray(content,r'.*WAP_STATUS.*')
    if wap_events is not None:
     tailId=re.search(r'.*?(?=\/)',relevantPart).group(0)
     try:
      avionicLogData[tailId]
     except Exception as e:
      avionicLogData[tailId]={}
     try:
      avionicLogData[tailId]['wap_status']
     except Exception as e:
      avionicLogData[tailId]['wap_status']={}
     for i,e in enumerate(wap_events):
      try:
       weTimestamp=re.search(r'.*?(?=\s\[)',e).group(0)
       weTimestamp=re.sub(r'[^0-9]','',weTimestamp)
       weStatus=int(re.search(r'(?<=status).*',e).group(0))
       avionicLogData[tailId]['wap_status'][weTimestamp]=weStatus
      except Exception as e:
       pass
  self.general.loggy('Writing '+self.settings.finalAvionicJson+'...')
  fo.writeJson(self.settings.finalAvionicJson,avionicLogData)
 def addFlightsToAvionicJson(self):
  print('\nTrying to group avionic json wap events by flights...')
  returnData={'dataset_id':'avionic'}
  avionicJson=fo.readJson(self.settings.finalAvionicJson)
  flightradarData=fo.readJson(self.settings.finalFlightradarJson)
  orderdataAggregated=fo.readJson(self.settings.finalOrderdataAggregatedJson)
  userdata=fo.readJson(self.settings.finalUserdataJson)
  revivedata=fo.readJson(self.settings.finalRevivedataJson)
  for f in flightradarData:
   self.general.loggy('Now at flight '+f+'...')
   flightdataset=flightradarData[f]
   fd=f.split(self.settings.uuidDelimiter)
   if len(fd)==3:
    fdTailId=fd[0]
    fdFlightNo=fd[1]
    fdDate=fd[2]
    try:
     fdDepartureTime=flightdataset['departure']['userdata_collection_timestamp']
    except Exception as e:
     fdDepartureTime=None
    try:
     fdArrivalTime=flightdataset['arrival']['userdata_collection_timestamp']
    except Exception as e:
     fdArrivalTime=None
    for avionicTailId in avionicJson:
     if avionicTailId.lower()==fdTailId.lower():
      uuid=avionicTailId.lower()+self.settings.uuidDelimiter+fdFlightNo+self.settings.uuidDelimiter+fdDate
      for wapEvent in avionicJson[avionicTailId]:
       try:
        returnData[uuid]
       except Exception as e:
        returnData[uuid]={}
       we=avionicJson[avionicTailId][wapEvent]
       doOrderdataExist=False
       doUserdataExist=False
       doRevivedataExist=False
       doWapEventsExist=False
       try:
        i=len(userdata[uuid])
        if i>0:
         doUserdataExist=True
       except Exception as e:
        self.general.loggy(e)
        pass
       try:
        i=orderdataAggregated[uuid]['no_of_cc_transactions']
        j=orderdataAggregated[uuid]['no_of_voucher_transactions']
        if i>0 or j>0:
         doOrderdataExist=True
       except Exception as e:
        self.general.loggy(e)
        pass
       try:
        lenrev=len(revivedata[uuid])
        if lenrev>1:
         doRevivedataExist=True
       except Exception as e:
        self.general.loggy(e)
        pass
       returnData[uuid]['do_orders_exist']=doOrderdataExist
       returnData[uuid]['do_revivedata_exist']=doRevivedataExist
       returnData[uuid]['do_userdata_exist']=doUserdataExist
       for w in we:
        if int(w)>int(fdDepartureTime)and int(w)<int(fdArrivalTime):
         try:
          returnData[uuid]['wap_status']
         except Exception as e:
          returnData[uuid]['wap_status']={}
         try:
          returnData[uuid]['wap_status'][w]
         except Exception as e:
          returnData[uuid]['wap_status'][w]={}
         try:
          returnData[uuid]['wap_status'][w]=we[w]
         except Exception as e:
          returnData[uuid]['wap_status'][w]={}
         returnData[uuid]['departure_userdata_collection_time']=fdDepartureTime
         returnData[uuid]['arrival_userdata_collection_time']=fdArrivalTime
         try:
          returnData[uuid]['wap_status']
         except Exception as e:
          self.general.loggy(e)
          pass
         else:
          doWapEventsExist=True
       returnData[uuid]['do_wapevents_exist']=doWapEventsExist
  self.general.loggy('Writing '+self.settings.finalAvionicAggregatedJson+'...')
  fo.writeJson(self.settings.finalAvionicAggregatedJson,returnData)
 def wasWapActive(self):
  self.general.loggy('Calculating if wap was on...')
  wapActiveTimerange=3000
  avionicByFlights=fo.readJson(self.settings.finalAvionicAggregatedJson)
  for flight in avionicByFlights:
   self.general.loggy('Now for flight '+flight+'...')
   try:
    if avionicByFlights[flight]['do_wapevents_exist']is True:
     wapActive=self.settings.stringOff
    else:
     wapActive=self.settings.stringNa
   except:
    wapActive=self.settings.stringNa
    pass
   arr=['do_orderdata_exist','do_userdata_exist','do_revivedata_exist']
   for a in arr:
    try:
     if avionicByFlights[flight][a]is True:
      wapActive=self.settings.stringOn
      break
    except Exception as e:
     self.general.loggy(e)
     pass
   try:
    wap_status=avionicByFlights[flight]['wap_status']
   except Exception as e:
    pass
   else:
    tempArr=[]
    for w in wap_status:
     timestamp=w
     status=wap_status[w]
     tempArr.append([timestamp,status])
    tempArr=sorted(tempArr,key=lambda x:x[0],reverse=False)
    for i,t in enumerate(tempArr):
     try:
      if tempArr[i][0]==0:
       diff=tempArr[i][0]-avionicByFlights[flight]['departure_userdata_collection_time']
       if diff>wapActiveTimerange:
        wapActive=self.settings.stringOn
        break
      if tempArr[i][1]==1 and tempArr[i+1][1]==0:
       diff=int(tempArr[i+1][0])-int(tempArr[i][0])
       if diff>wapActiveTimerange:
        wapActive=self.settings.stringOn
        break
      if tempArr[i][-1]==1:
       diff=avionicByFlights[flight]['arrival_userdata_collection_time']-tempArr[i][-1]
       if diff>wapActiveTimerange:
        wapActive=self.settings.stringOn
        break
     except Exception as e:
      self.general.loggy(e)
      pass
   try:
    avionicByFlights[flight]['wap_was_active']=wapActive
   except Exception as e:
    pass
  avionicByFlights['dataset_id']='avionic_aggregated'
  self.general.loggy('Writing '+self.settings.finalAvionicAggregatedJson+' and returning data...')
  fo.writeJson(self.settings.finalAvionicAggregatedJson,avionicByFlights)
 def parseFlightlog(self):
  flightlogData={}
  self.general.loggy('Merging flight.log data into overall...')
  rx=r'flight\.log$'
  files=fo.findFiles(self.settings.tmpdir,rx,True,True)
  for f in files:
   filecontent=fo.readFile(f)
   for l in filecontent:
    rx=r'(\{.*)(\{.*"Flight_Phase\":\s\"TAXI\".*?\})'
    try:
     relpart=re.search(rx,l).group(0)
    except Exception as e:
     self.general.loggy(e)
     pass
    else:
     line={}
     relpart=json.loads(relpart)
     tid=relpart['Aircraft_Tail_Number'].lower()
     fnr=relpart['Flight_Number'].lower()
     dat=re.sub(r'[^0-9]*','',relpart['Date'])
     dat='20'+dat[-2:]+dat[2:4]+dat[0:2]
     uuid=tid+'_'+fnr+'_'+dat
     line[uuid]=relpart
     flightlogData[uuid]=line
     break
   self.general.loggy('Writing '+self.settings.finalFlightlogJson+'...')
   fo.writeJson(self.settings.finalFlightlogJson,flightlogData)
 def iterateOrderdataFlights(self):
  self.general.loggy('\nIterating over the orderdata of the flights...')
  orderdata=fo.readJson(self.settings.finalOrderdataJson)
  orderdataAggregated={}
  for o in orderdata:
   oneFlightKey=o
   oneFlightDataset=orderdata[o]
   orderdataAggregated=self.aggregators.aggregateOrderdata(orderdataAggregated,oneFlightKey,oneFlightDataset)
  orderdataAggregated['dataset_id']='orderdata_aggregated'
  fo.writeJson(self.settings.finalOrderdataAggregatedJson,orderdataAggregated)
