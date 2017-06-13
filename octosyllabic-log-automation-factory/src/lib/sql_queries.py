import json,re
from lib.file_ops import fileOps as fo
from lib.general import general
class sqlQueries:
 def __init__(self,settings):
  self.settings=settings
  self.general=general(self.settings)
 def queryOrderdata(self,tailId,startdate,enddate):
  query='"SELECT json_agg(row_to_json(tbl)) AS jsondata FROM (SELECT '+ 'id, reference, product_reference, tail_nr,flight_nr,'+ 'cap_user_id, origin_icao, destination_icao, imported_date,'+ 'currency, conversion_rate, unit_price, product_quantity,'+ 'product_name, product_supplier_reference, supplier_reference,'+ 'supplier_name, current_state, invoice_date, invoice_address_firstname,'+ 'invoice_address_lastname, invoice_address_address1, invoice_address_address2,'+ 'invoice_address_postcode, invoice_address_city, invoice_address_other,'+ 'invoice_address_phone, invoice_address_phone_mobile, accomodation_email,'+ 'accomodation_phone, accomodation_address_summary, voucher_code, voucher_code_created,'+ 'payment_status, payment_status_description, modified_date, is_processed, uri '+ 'FROM bucket."order" AS od WHERE '+ 'tail_nr = \''+tailId+'\' '+ 'AND invoice_date BETWEEN \''+startdate+'\' AND \''+enddate+'\') AS tbl;"'
  return(self.runQuery(query,'orderdata'))
 def queryUserdata(self,tailId,startdate,enddate):
  query='"SELECT json_agg(row_to_json(ud.*)) AS jsondata '+ 'FROM bucket.user ud '+ 'WHERE tail_nr = \''+tailId+'\' '+ 'AND created_date BETWEEN \''+startdate+'\' AND \''+enddate+'\' ;"'
  return(self.runQuery(query,'userdata'))
 def queryRevivedata(self,tailId,startdate,enddate,origin,destination,campaign=None):
  query='"SELECT json_agg(row_to_json(tbl)) AS jsondata '+ 'FROM ( SELECT '+ 's.date_time AS date_time, '+ 'SUM(s.impressions) AS sum_views, '+ 'SUM(s.clicks) AS sum_clicks, '+ 's.tail_nr, '+ 's.flight_nr, '+ 's.origin_icao, '+ 's.destination_icao, '+ 'cs.campaignname '+ 'FROM bucket.rv_data_summary_ad_hourly AS s '+ 'LEFT JOIN bucket.rv_banners AS bs '+ 'ON bs.bannerid = s.ad_id '+ 'LEFT JOIN bucket.rv_campaigns AS cs '+ 'ON cs.campaignid = bs.campaignid '+ 'WHERE s.date_time >= \''+startdate+'\' '+ 'AND s.date_time <= \''+enddate+'\''+ 'AND s.tail_nr = \''+tailId+'\' '+ 'AND s.origin_icao = \''+origin+'\' '+ 'AND s.destination_icao = \''+destination+'\' '+ 'GROUP BY s.tail_nr, s.flight_nr, s.origin_icao, '+ 's.destination_icao, cs.campaignname, s.date_time'+ ') AS tbl;"'
  return(self.runQuery(query,'revivedata'))
 def runQuery(self,query,datatype):
  cmd=self.settings.psqlRequest[:-3]+'-c '+query
  print(str(datatype).title()+' query...')
  self.general.loggy(str(datatype).title()+' query: '+str(cmd),True)
  r={}
  try:
   r=fo.runCmd(cmd)
  except Exception as e:
   self.general.loggy(e)
   pass
  r=re.sub(r'(\n|\r|\t)','',r)
  if r==' ':
   r={}
  try:
   r=json.loads(r)
  except Exception as e:
   self.general.loggy(e)
  return(r)
 def sqlQueryIterator(self):
  self.general.loggy('\nQuerying SQL database containing user data...')
  orderdata={}
  userdata={}
  revivedata={}
  flightradarData=fo.readJson(self.settings.finalFlightradarJson)
  for d in flightradarData:
   try:
    udc_dep=flightradarData[d]['departure']['userdata_collection_time']
    udc_arr=flightradarData[d]['arrival']['userdata_collection_time']
    tailId=flightradarData[d]['aircraft']['registration']
    origin=flightradarData[d]['airport']['origin']['code']['icao']
    destination=flightradarData[d]['airport']['destination']['code']['icao']
   except Exception as e:
    orderdataline={}
    userdataline={}
    revivedataline={}
    pass
   else:
    try:
     userdataline=self.queryUserdata(tailId,udc_dep,udc_arr)
    except Exception as e:
     userdataline={}
    try:
     orderdataline=self.queryOrderdata(tailId,udc_dep,udc_arr)
    except Exception as f:
     orderdataline={}
    try:
     revivedataline=self.queryRevivedata(tailId,udc_dep,udc_arr,origin,destination)
    except Exception as f:
     revivedataline={}
   userdata[d]=userdataline
   orderdata[d]=orderdataline
   revivedata[d]=revivedataline
  userdata['dataset_id']='userdata'
  orderdata['dataset_id']='orderdata'
  revivedata['dataset_id']='revivedata'
  self.general.loggy('Writing orderdata, userdata and revivedata into json files...')
  fo.writeJson(self.settings.finalOrderdataJson,orderdata)
  fo.writeJson(self.settings.finalUserdataJson,userdata)
  fo.writeJson(self.settings.finalRevivedataJson,revivedata)
