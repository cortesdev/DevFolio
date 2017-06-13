import argparse
from lib.file_ops import fileOps as fo
import lib.archiver
import lib.aggregators
import lib.data_joiner
import lib.flightradar24
import lib.general
import lib.log_parsers
import lib.logs_to_local
import lib.mailjet
import lib.presets
import lib.settings
import lib.sql_queries
import lib.writer_csv
import lib.writer_xlsx
pre=lib.presets.presets()
parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description='octosyllabic log automation factory [olaf]',)
parser.add_argument('-f','--filter_tail_id',type=str,default=None,help='filter tail id')
parser.add_argument('-fx','--filter_tail_id_regex',type=pre.checkRegexScheme,default=None,help='filter tail id(s) by regex scheme (i.e. for multiple ids: "(g-tcdx|g-tcdy)" or for ids beginning with g-: "g-.*")')
parser.add_argument('-s','--start_time',type=pre.mkdate,default=pre.getDateString('begin',6),help='start time of the timespan which the report will cover, required format \"YYYY-MM-DD\"')
parser.add_argument('-e','--end_time',type=pre.mkdate,default=pre.getDateString('end',0),help='end time of the timespan which the report will cover, required format \"YYYY-MM-DD\"')
parser.add_argument('-td','--timespan_data_collection',type=int,default=7,help='days back that the report will generate data for, is relative to start time, default is start time +7 days back')
parser.add_argument('-tf','--timespan_file_sync',type=int,default=5,help='time range of the files that will be pulled from the groundserver, usually relative to the timespan of the data collection, default is start of data collection +5 days back')
parser.add_argument('--sendmail',action='store_true',default=False,help='send report by mail to recipients defined in list')
parser.add_argument('-d','--debug',action='store_true',default=False,help='debug mode, for quick test, does not sync or extract files')
parser.add_argument('-y','--yes',action='store_true',default=False,help='assume yes on all queries')
args=parser.parse_args()
if args.end_time['posix']!=pre.getDateString('end',0)['posix']and args.start_time['posix']==pre.getDateString('begin',6)['posix']:
 args.start_time=pre.mkdate(args.end_time['string'],args.timespan_data_collection)
args.timespan_data_collection=pre.calculateDataSyncTimespan(args.start_time['dateobj'])
args.timespan_file_sync=args.timespan_data_collection+args.timespan_file_sync
settings=lib.settings.settings(args)
settings.emptyLogFile()
gen=lib.general.general(settings)
if args.filter_tail_id is not None:
 settings.dataCommercialAcList=gen.filterTailIdList(args.filter_tail_id,'string')
if args.filter_tail_id_regex is not None:
 settings.dataCommercialAcList=gen.filterTailIdList(args.filter_tail_id_regex,'regex')
if args.filter_tail_id is not None or args.filter_tail_id_regex is not None:
 gen.queryOnFilterResults(settings.dataCommercialAcList)
arc=lib.archiver.archiver(settings)
djo=lib.data_joiner.dataJoiner(settings)
fr24=lib.flightradar24.flightradar24(settings)
gen=lib.general.general(settings)
mail=lib.mailjet.mailjet(settings)
l2l=lib.logs_to_local.logsToLocal(settings)
lpa=lib.log_parsers.logParsers(settings)
sql=lib.sql_queries.sqlQueries(settings)
agg=lib.aggregators.aggregators(settings)
w2c=lib.writer_csv.csvWriter(settings)
xls=lib.writer_xlsx.excelWriter(settings)
gen.loggy('Starting OLAF with the following settings: '+str(args))
gen.dropPid()
l2l.doSyncToLocal()
l2l.doSyncToTemp()
l2l.extractAll()
fr24.syncAndParseFlightradar() 
lpa.parseOverallStats() 
lpa.parseAvionicLogs() 
sql.sqlQueryIterator() 
lpa.iterateOrderdataFlights() 
agg.aggregateRevivedata() 
lpa.addFlightsToAvionicJson() 
lpa.wasWapActive() 
djo.joinAll([fo.readJson(settings.finalFlightradarJson),fo.readJson(settings.finalOverallJson),fo.readJson(settings.finalOrderdataJson),fo.readJson(settings.finalOrderdataAggregatedJson),fo.readJson(settings.finalRevivedataAggregatedJson),fo.readJson(settings.finalUserdataJson),fo.readJson(settings.finalAvionicAggregatedJson)])
finaldata=w2c.writeCsv() 
xls.writeXlsx(finaldata) 
arc.doArchive() 
mail.sendReport() 
gen.deletePid()
