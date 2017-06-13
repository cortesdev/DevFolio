from lib.file_ops import fileOps as fo
from lib.general import general
from lib.data_joiner import dataJoiner
class csvWriter:
 def __init__(self,settings):
  self.settings=settings
  self.general=general(self.settings)
  self.djo=dataJoiner(self.settings)
  self.csvHeader=[]
 def beautifyEuroValues(self,val,decimals):
  val=round(val,decimals)
  if val==0:
   val='0.0'
  val=self.commatize(val)
  while len(val)<decimals+2:
   val+='0'
  return(val)
 def commatize(self,val):
  val=str(val)
  try:
   val=val.replace('.',',')
  except Exception as e:
   pass
  return(val)
 def getValue(self,dictionary,accessor,r=''):
  if len(accessor)==1:
   try:
    return(dictionary[accessor[0]])
   except Exception as e:
    return(r)
  elif len(accessor)==2:
   try:
    return(dictionary[accessor[0]][accessor[1]])
   except Exception as e:
    return(r)
  elif len(accessor)==3:
   try:
    return(dictionary[accessor[0]][accessor[1]][accessor[2]])
   except Exception as e:
    return(r)
  elif len(accessor)==4:
   try:
    return(dictionary[accessor[0]][accessor[1]][accessor[2]][accessor[3]])
   except Exception as e:
    return(r)
  elif len(accessor)==5:
   try:
    return(dictionary[accessor[0]][accessor[1]][accessor[2]][accessor[3]][accessor[4]])
   except Exception as e:
    return(r)
  else:
   return(r)
 def userCount(self,userdata,timestamp):
  if len(userdata)<1:
   age=int(self.settings.timestampToday)-int(timestamp)
   if age<=3:
    return(self.settings.stringNyr)
   else:
    return(self.settings.stringNa)
  else:
   return(len(userdata))
 def lineAppendix(self,headerVal,lineVal,line):
  detected=False
  for h in self.csvHeader:
   if h==headerVal:
    detected=True
    break
  if detected is False:
   self.csvHeader.append(headerVal)
  line.append(lineVal)
  return(line)
 def writeCsv(self):
  joinedData=fo.readJson(self.settings.finalJoinedDataJson)
  self.general.loggy('\nFinally writing a csv file...')
  tempCsv=[]
  for j in joinedData:
   jj=joinedData[j]
   line=[]
   a=self.getValue(jj,['flightradar','departure','date'],None)
   b=self.getValue(jj,['flightradar','aircraft','registration'],None)
   c=self.getValue(jj,['flightradar','identification','number','default'],None)
   line=self.lineAppendix('sort index',str(a)+str(b)+str(c),line)
   a=self.getValue(jj,['flightradar','commercial_flight'],None)
   if a is True:
    line=self.lineAppendix('Commercial','yes',line)
   else:
    line=self.lineAppendix('Commercial','no',line)
   a=str(self.general.digger(self.getValue(jj,['flightradar','departure','day'],None),2,0))
   b=str(self.general.digger(self.getValue(jj,['flightradar','departure','month'],None),2,0))
   c=str(self.getValue(jj,['flightradar','departure','year'],None))
   if a is None or b is None or c is None:
    line=self.lineAppendix('Date',self.settings.stringNone,line)
   else:
    line=self.lineAppendix('Date',a+'.'+b+'.'+c,line)
   a=self.getValue(jj,['flightradar','departure','year'],None)
   b=self.getValue(jj,['flightradar','departure','week_of_year'],None)
   line=self.lineAppendix('Week',str(a)+'-'+str(b),line)
   line=self.lineAppendix('Tail No',self.getValue(jj,['flightradar','aircraft','registration']),line)
   line=self.lineAppendix('Flight No',self.getValue(jj,['flightradar','flight_no']),line)
   line=self.lineAppendix('IATA FNo.',self.getValue(jj,['flightradar','identification','number','default']),line)
   line=self.lineAppendix('Origin',self.getValue(jj,['flightradar','airport','origin','code','icao']),line)
   line=self.lineAppendix('Destination',self.getValue(jj,['flightradar','airport','destination','code','icao']),line)
   line=self.lineAppendix('Duration',self.getValue(jj,['flightradar','flight_duration']),line)
   w=self.getValue(jj,['avionic_aggregated','wap_was_active'],self.settings.stringNa)
   a=self.getValue(jj,['userdata'],None)
   b=self.getValue(jj,['flightradar','arrival','date'],None)
   if a is None or b is None:
    a=self.settings.stringNone
   else:
    a=self.userCount(a,b)
   if a==self.settings.stringNyr:
    w=a
   try:
    if a>0:
     w=self.settings.stringOn
   except Exception as e:
    self.general.loggy(e)
    pass
   line=self.lineAppendix('WAP',w,line)
   line=self.lineAppendix('No Users',a,line)
   line=self.lineAppendix('No CC TAs',self.getValue(jj,['orderdata_aggregated','no_of_cc_transactions']),line)
   line=self.lineAppendix('Val CC TAs',self.beautifyEuroValues(self.getValue(jj,['orderdata_aggregated','val_of_cc_transactions']),4),line)
   line=self.lineAppendix('No Vouchers',self.getValue(jj,['orderdata_aggregated','no_of_voucher_transactions']),line)
   line=self.lineAppendix('Val Vouchers',self.beautifyEuroValues(self.getValue(jj,['orderdata_aggregated','val_of_voucher_transactions']),4),line)
   line=self.lineAppendix('No SEPs',self.getValue(jj,['orderdata_aggregated','no_of_single_eps']),line)
   line=self.lineAppendix('Val SEPs',self.beautifyEuroValues(self.getValue(jj,['orderdata_aggregated','val_of_single_eps']),4),line)
   line=self.lineAppendix('No FEPs',self.getValue(jj,['orderdata_aggregated','no_of_family_eps']),line)
   line=self.lineAppendix('Val FEPs',self.beautifyEuroValues(self.getValue(jj,['orderdata_aggregated','val_of_family_eps']),4),line)
   line=self.lineAppendix('No Magz',self.getValue(jj,['orderdata_aggregated','no_of_magazine_purchases']),line)
   line=self.lineAppendix('Val Magz',self.beautifyEuroValues(self.getValue(jj,['orderdata_aggregated','val_of_magazine_purchases']),4),line)
   line=self.lineAppendix('No DstSrv',self.getValue(jj,['orderdata_aggregated','no_of_destination_service_purchases']),line)
   line=self.lineAppendix('Val DstSrv',self.beautifyEuroValues(self.getValue(jj,['orderdata_aggregated','val_of_destination_service_purchases']),4),line)
   line=self.lineAppendix('Total TA Value',self.beautifyEuroValues(self.getValue(jj,['orderdata_aggregated','total_transaction_value']),4),line)
   line=self.lineAppendix('Valora Views',self.getValue(jj,['revivedata_aggregated','Valora - Default Campaign','sum_views']),line)
   line=self.lineAppendix('Valora Clicks',self.getValue(jj,['revivedata_aggregated','Valora - Default Campaign','sum_clicks']),line)
   line=self.lineAppendix('Sprungraum Views',self.getValue(jj,['revivedata_aggregated','Sprungraum - Default Campaign','sum_views']),line)
   line=self.lineAppendix('Sprungraum Clicks',self.getValue(jj,['revivedata_aggregated','Sprungraum - Default Campaign','sum_clicks']),line)
   if len(line)>1:
    tempCsv.append(line)
  tempCsv=sorted(tempCsv,key=lambda x:x[0],reverse=False)
  finalCsv=[self.csvHeader[1:]]
  for t in tempCsv:
   finalCsv.append(t[1:])
  fo.writeCsv(self.settings.finalJoinedDataCsv,finalCsv)
  return(finalCsv)
