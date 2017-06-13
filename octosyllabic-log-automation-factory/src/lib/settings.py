from lib.file_ops import fileOps as fo
import datetime,re,time
class settings:
 def __init__(self,args):
  self.startTime=datetime.datetime.now()
  self.args=args
  self.fo=fo
  self.scriptdir=self.detectFolder(['/home/olaf/scripts/python/octosyllabic-log-automation-factory/','/var/'],r'main.py$')
  self.voldir='/var/olaf_volume/'
  self.staticdir=self.voldir+'static/'
  self.dbdir=self.voldir+'db/'
  self.cfgdir=self.voldir+'cfg/'
  self.tmpdir=self.voldir+'tmp/'
  self.rxValidUuid=r'^[a-z]{0,4}-[a-z]{0,4}_[a-z0-9]+_([1,2][0][0,1,2,3][0-9][0-9]{4}|None)$'
  self.rxFlightNoReduction=r'(.*?_([a-zA-Z]+[0-9]+|[a-zA-Z]+)).*?(_[0-9]+)'
  self.rxIsFlightNoComplex=r'.*?_([a-zA-Z]+[0-9]+[a-zA-Z]+).*?_[0-9]+'
  self.uuidDelimiter='_'
  self.rsyncBase='rsync -avm --min-size=1'
  self.datadirRemoteBase='paxlife@172.18.102.76:/data/'
  self.datadirRemoteArr=['in/avionic/','in/media4sky/']
  self.psqlRequest='psql -h 172.18.102.72 -d paxlife_dwh -U elk_svc -w -t -f '
  self.datadirLocalLogfiles=self.dbdir+'sync_from_groundserver/'
  self.datadirLocalSql=self.dbdir+'sql/report_per_flight.json'
  self.datadirLocalTmpExtracted=self.tmpdir+'extracted/'
  self.datadirLocalTmpCorrupted=self.tmpdir+'corrupted/'
  self.datadirFlightradar=self.dbdir+'flightradar/'
  self.finalOutFolder=self.staticdir+'output/'
  self.finalFlightradarJson=self.finalOutFolder+'flightradar.json'
  self.finalOverallJson=self.finalOutFolder+'overall_stats.json'
  self.finalUserdataJson=self.finalOutFolder+'userdata.json'
  self.finalOrderdataJson=self.finalOutFolder+'orderdata.json'
  self.finalRevivedataJson=self.finalOutFolder+'revivedata.json'
  self.finalOrderdataAggregatedJson=self.finalOutFolder+'orderdata_agg.json'
  self.finalRevivedataAggregatedJson=self.finalOutFolder+'revivedata_agg.json'
  self.finalFlightlogJson=self.finalOutFolder+'flightlog.json'
  self.finalAvionicJson=self.finalOutFolder+'avionic.json'
  self.finalAvionicAggregatedJson=self.finalOutFolder+'avionic_agg.json'
  self.finalJoinedDataJson=self.finalOutFolder+'finally_joined_data.json'
  self.finalJoinedDataCsv=self.staticdir+'reports/report_'+self.getTimestamp()+'.csv'
  self.finalJoinedDataXlsx=self.staticdir+'reports/report_'+self.getTimestamp()+'.xlsx'
  self.dataCommercialAcList=fo.readJson(self.cfgdir+'commercial_tail_ids.json')
  self.timestamp=self.getTimestamp()
  self.timestampToday=int(self.getTimestamp('-').split('-')[0])
  self.archiverFolder=self.staticdir+'archive/'
  self.archiverTargetfile=self.archiverFolder+self.timestamp+'.zip'
  self.mailjetRecipients=self.cfgdir+'mailjet_report_recipients.json'
  self.logfile=self.staticdir+'log/olaf.log'
  self.stringNa='NA'
  self.stringNyr='NYR'
  self.stringOn='ON'
  self.stringOff='OFF'
  self.stringNone='None'
  self.stringAmbiguous='Ambiguous'
 def emptyLogFile(self):
  open(self.logfile,'w').close()
 def getTimestamp(self,sep='-'):
  t=time.strftime('%Y%m%d'+sep+'%H%M%S')
  return(t)
 def calculateDelta(self):
  t=int(str(self.timestampToday)[-2:])
  d=self.timestampDeltaDiff
  if t<7:
   d=d+70
  deltastamp=self.timestampToday-d
  print('\nGetting all flights before '+str(deltastamp)+'...')
  return(deltastamp)
 def detectFolder(self,folderlist,rxFinder):
  for f in folderlist:
   try:
    r=self.fo.findFiles(f,rxFinder,True,True)[0]
   except Exception as e:
    print(e)
    pass
   else:
    break
  r=re.search(r'.*\/',r).group(0)
  return(r)
