import flask,os
from shelljob import proc
from random import choice
app=flask.Flask(__name__,static_url_path='',static_folder='/var/olaf_volume/static/')
def isOlafCreatingReport():
 return(os.path.isfile('/tmp/olaf.pid'))
@app.route('/')
def list_reports():
 basedir='/var/olaf_volume/static/'
 archivedir=basedir+'archive/'
 reportsdir=basedir+'reports/'
 outputdir=basedir+'output/'
 logdir=basedir+'log/'
 archive=sorted(os.listdir(archivedir),reverse=True)
 reports=sorted(os.listdir(reportsdir),reverse=True)
 output=sorted(os.listdir(outputdir),reverse=False)
 logs=sorted(os.listdir(logdir),reverse=False)
 isRunning=isOlafCreatingReport()
 return flask.render_template('index.html',reports=reports,output=output,logs=logs,archive=archive,isRunning=isRunning)
@app.route('/create-new-report',methods=['GET','POST'])
def send_to_all():
 g=proc.Group()
 p=g.run(['python3',app.root_path+'/src/main.py'])
 def read_process():
  while g.is_pending():
   lines=g.readlines()
   for proc,line in lines:
    yield line
 return flask.Response(read_process(),mimetype='text/plain')
 pass
@app.errorhandler(404)
def page_not_found(e):
 return(flask.redirect('/'))
if __name__=='__main__':
 app.run(debug=False,host='0.0.0.0',port=5555)
