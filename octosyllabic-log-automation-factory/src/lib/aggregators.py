from lib.file_ops import fileOps as fo
from lib.general import general
from lib.writer_csv import csvWriter
import json
class aggregators:
 def __init__(self,settings):
  self.settings=settings
  self.general=general(self.settings)
  self.csvw=csvWriter(self.settings)
 def makeItEuros(self,val,isoCode,conversionRate):
  if isoCode!='EUR':
   val=val/conversionRate
  return(val)
 def aggregateOrderdata(self,orderdataAggregated,oneFlightKey,oneFlightDataset):
  self.general.loggy('Aggregating orderdata of '+oneFlightKey+'...')
  no_of_cc_transactions=0
  val_of_cc_transactions=0
  no_of_voucher_transactions=0
  val_of_voucher_transactions=0
  no_of_single_eps=0
  val_of_single_eps=0
  no_of_family_eps=0
  val_of_family_eps=0
  no_of_magazine_purchases=0
  val_of_magazine_purchases=0
  no_of_destination_service_purchases=0
  val_of_destination_service_purchases=0
  for jd in oneFlightDataset:
   try:
    json.dumps(jd,sort_keys=True,indent=4)
   except Exception as e:
    self.general.loggy(e)
    pass
   else:
    try:
     int(jd['current_state'])
    except Exception as e:
     pass
    else:
     if jd['current_state']==209:
      no_of_cc_transactions+=1
      val_of_cc_transactions+=self.makeItEuros(float(jd['unit_price']*float(jd['product_quantity'])),jd['currency'],float(jd['conversion_rate']))
     if jd['current_state']==220:
      no_of_voucher_transactions+=1
      val_of_voucher_transactions+=self.makeItEuros(float(jd['unit_price']*float(jd['product_quantity'])),jd['currency'],float(jd['conversion_rate']))
     if (jd['current_state']==209 or jd['current_state']==220) and jd['product_reference']=='ENTERTAINMENT_PACKAGE':
      no_of_single_eps+=float(jd['product_quantity'])
      val_of_single_eps+=self.makeItEuros(float(jd['unit_price']*float(jd['product_quantity'])),jd['currency'],float(jd['conversion_rate']))
     if (jd['current_state']==209 or jd['current_state']==220) and jd['product_reference']=='ENTERTAINMENT_PACKAGE_FAMILY':
      no_of_family_eps+=float(jd['product_quantity'])
      val_of_family_eps+=self.makeItEuros(float(jd['unit_price']*float(jd['product_quantity'])),jd['currency'],float(jd['conversion_rate']))
     if(jd['current_state']==209 or jd['current_state']==220)and jd['supplier_name']=='Media Carrier':
      no_of_magazine_purchases=float(jd['product_quantity'])
      val_of_magazine_purchases+=self.makeItEuros(float(jd['unit_price']*float(jd['product_quantity'])),jd['currency'],float(jd['conversion_rate']))
     if(jd['current_state']==209 or jd['current_state']==220)and str(jd['product_reference']).startswith('Iberoservice')is True:
      no_of_destination_service_purchases=float(jd['product_quantity'])
      val_of_destination_service_purchases+=self.makeItEuros(float(jd['unit_price']*float(jd['product_quantity'])),jd['currency'],float(jd['conversion_rate']))
  aggregatedFlightDataset={}
  aggregatedFlightDataset['no_of_cc_transactions']=int(no_of_cc_transactions)
  aggregatedFlightDataset['val_of_cc_transactions']=val_of_cc_transactions
  aggregatedFlightDataset['no_of_voucher_transactions']=int(no_of_voucher_transactions)
  aggregatedFlightDataset['val_of_voucher_transactions']=val_of_voucher_transactions
  aggregatedFlightDataset['no_of_single_eps']=int(no_of_single_eps)
  aggregatedFlightDataset['val_of_single_eps']=val_of_single_eps
  aggregatedFlightDataset['no_of_family_eps']=int(no_of_family_eps)
  aggregatedFlightDataset['val_of_family_eps']=val_of_family_eps
  aggregatedFlightDataset['no_of_magazine_purchases']=int(no_of_magazine_purchases)
  aggregatedFlightDataset['val_of_magazine_purchases']=val_of_magazine_purchases
  aggregatedFlightDataset['no_of_destination_service_purchases']=int(no_of_destination_service_purchases)
  aggregatedFlightDataset['val_of_destination_service_purchases']=val_of_destination_service_purchases
  aggregatedFlightDataset['total_transaction_value']=val_of_cc_transactions+val_of_voucher_transactions
  orderdataAggregated[oneFlightKey]=aggregatedFlightDataset
  return(orderdataAggregated)
 def getReviveCampaignNames(self,singleFlightDs):
  campaignNames=[]
  for d in singleFlightDs:
   self.general.waitOnKey
   cn=self.csvw.getValue(d,['campaignname'],None)
   if cn is not None and cn not in campaignNames:
    campaignNames.append(cn)
  return(campaignNames)
 def aggregateRevivedata(self):
  revivedata=fo.readJson(self.settings.finalRevivedataJson)
  revivedataAgg={'dataset_id':'revivedata_aggregated'}
  for uuid in revivedata:
   campaignNames=self.getReviveCampaignNames(revivedata[uuid])
   campaignHours=revivedata[uuid]
   for cn in campaignNames:
    sc=0
    sv=0
    for ch in campaignHours:
     if cn==self.csvw.getValue(ch,['campaignname']):
      sc+=self.csvw.getValue(ch,['sum_clicks'],0)
      sv+=self.csvw.getValue(ch,['sum_views'],0)
    try:
     revivedataAgg[uuid]
    except:
     revivedataAgg[uuid]={}
    else:
     pass
    try:
     revivedataAgg[uuid][cn]
    except Exception as e:
     revivedataAgg[uuid][cn]={'sum_clicks':0,'sum_views':0}
    else:
     pass
    finally:
     revivedataAgg[uuid][cn]['sum_clicks']=sc
     revivedataAgg[uuid][cn]['sum_views']=sv
  fo.writeJson(self.settings.finalRevivedataAggregatedJson,revivedataAgg)
