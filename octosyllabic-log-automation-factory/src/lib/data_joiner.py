from lib.file_ops import fileOps as fo
from lib.general import general
import re
class dataJoiner:
 def __init__(self,settings):
  self.settings=settings
  self.general=general(settings)
 def mergeTwoJsonDatasets(self,dic1,dic2):
  returnData=dic1
  for uuid1 in returnData:
   uuid1ToCompare=self.shrinkUuid(uuid1)
   for uuid2 in dic2:
    try:
     if bool(re.search(self.settings.rxIsFlightNoComplex,uuid2))is True:
      if uuid1==uuid2:
       returnData[uuid1][dic2['dataset_id']]=dic2[uuid2]
     else:
      if uuid1ToCompare==uuid2:
       returnData[uuid1][dic2['dataset_id']]=dic2[uuid2]
    except Exception as e:
     print(e)
     pass
  return(returnData)
 def shrinkUuid(self,uuid):
  try:
   m=re.search(self.settings.rxFlightNoReduction,uuid)
   uuid=m.group(1)+m.group(3)
  except Exception as e:
   pass
  return(uuid)
 def joinAll(self,dicArr):
  returnData={}
  basedic=dicArr[0]
  for d in basedic:
   did=basedic['dataset_id']
   if d!='dataset_id':
    returnData[d]={}
    returnData[d][did]=basedic[d]
  for dic in dicArr[1:]:
   returnData=self.mergeTwoJsonDatasets(returnData,dic)
  self.general.loggy('Writing '+self.settings.finalJoinedDataJson+'...')
  fo.writeJson(self.settings.finalJoinedDataJson,returnData)
