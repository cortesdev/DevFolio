import math,re,xlsxwriter
from lib.general import general
class excelWriter:
 def __init__(self,settings):
  self.settings=settings
  self.general=general(self.settings)
  self.workbook=xlsxwriter.Workbook(self.settings.finalJoinedDataXlsx)
  self.worksheet=self.workbook.add_worksheet('Automatic Report')
  self.formatBold=self.workbook.add_format({'bold':1})
  self.formatBoldTop=self.workbook.add_format({'bold':1,'top':1})
  self.formatClean=self.workbook.add_format({})
  self.formatDate=self.workbook.add_format({'num_format':'dd.mm.yyyy'})
  self.formatTime=self.workbook.add_format({'num_format':'HH.MM.SS'})
  self.formatMerge=self.workbook.add_format({'align':'right','bold':1})
  self.formatMergeTop=self.workbook.add_format({'align':'right','bold':1,'top':1})
  self.formatPrize=self.workbook.add_format({'num_format':'0.0000'})
  self.formatSums=self.workbook.add_format({'bold':1,'top':1})
 def excelIdx(self,val):
  idx=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  return(idx[val])
 def addSumFormulaBelow(self,pos,formulaRange):
  formula='{=SUM('+formulaRange+')}'
  self.worksheet.write_formula(pos,formula,self.formatSums)
 def writeXlsx(self,data):
  self.general.loggy('\nWriting xlsx now...')
  noRows=len(data)
  noCols=len(data[0])
  rangeAutofilter=self.xlCoordinateConstructor(0,0,noCols-1,noRows-1)
  self.worksheet.autofilter(rangeAutofilter)
  for idxRow,line in enumerate(data):
   lenCol=len(data)-1
   lenMax=0
   for idxCol,el in enumerate(line):
    if idxRow==0:
     shape=self.workbook.add_format({'bold':1})
    else:
     shape=self.workbook.add_format({})
    if isinstance(el,str)is True:
     if bool(re.search(r'[0-9]+\,[0-9]+',el))is True:
      el=str(el.replace(',','.'))
      el=float(el)
      self.worksheet.write(idxRow,idxCol,el,self.formatPrize)
      self.addSumFormulaBelow(self.xlCoordinateConstructor(idxCol,lenCol+1),self.xlCoordinateConstructor(idxCol,1,idxCol,lenCol))
     elif bool(re.search(r'[0-9]{2}\.[0-9]{2}\.[0-9]{4}',el))is True:
      self.worksheet.write(idxRow,idxCol,el,self.formatDate)
     elif bool(re.search(r'[0-9]{1,2}:[0-9]{2}:[0-9]{2}',el))is True:
      self.worksheet.write(idxRow,idxCol,el,self.formatTime)
     else:
      self.worksheet.write_string(idxRow,idxCol,el,shape)
    elif isinstance(el,int)is True:
     self.worksheet.write_number(idxRow,idxCol,el,shape)
     self.addSumFormulaBelow(self.xlCoordinateConstructor(idxCol,lenCol+1),self.xlCoordinateConstructor(idxCol,1,idxCol,lenCol))
    if len(str(el))>lenMax:
     lenMax=len(str(el))
    if idxRow==0:
     self.worksheet.set_column(self.xlCoordinateConstructor(idxCol,0,idxCol,lenCol),lenMax*1.2)
  self.worksheet.freeze_panes(1,0)
  self.workbook.close()
 def xlCoordinateConstructor(self,x1,y1,x2=None,y2=None):
  y1+=1
  if y2 is not None:
   y2+=1
  letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  ll=float(len(letters))
  def calculateXParams(val):
   nol=math.floor(val/ll)+1
   if nol>1:
    pol=int(val%ll)
   else:
    pol=int(val)
   if nol>1:
    finalletters=letters[nol-2]+letters[pol]
   else:
    finalletters=letters[pol]
   return([nol,pol,finalletters])
  p=calculateXParams(x1)
  finalCoord=p[2]+str(y1)
  if x2 is not None:
   p=calculateXParams(x2)
   finalCoord+=':'+p[2]+str(y2)
  return(finalCoord)
