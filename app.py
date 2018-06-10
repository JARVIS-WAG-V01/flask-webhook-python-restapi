import json
import os
import requests
import pickle
import pandas as pd
import cloudant
from cloudant import Cloudant
from docx import Document
import time
from flask import Flask , request, make_response , render_template, session,g
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey,QueryResult

user= "000d5b69-974a-4f7b-9118-5bcb7aed2484-bluemix"
password= "ecab228d0b549390a55b708bcfe28f6818e223aa5761dc2628e65859c7211e87"
host= "000d5b69-974a-4f7b-9118-5bcb7aed2484-bluemix.cloudant.com"
url = 'https://' + host
client = Cloudant(user, password, url=url, connect=True)    
app = Flask(__name__)
app.config['SECRET_KEY']="QWERTYUIOPASDFGHJKLZXCVBNM"

@app.route('/webhook',methods=['POST'])
def webhook():
#    try:
    req=request.get_json(silent=True,force=True)
    sessionId=req.get("sessionId")
    print(sessionId)
    result=req.get("result")
    print(result)
    action=result.get("action")
    print(action)
    context=result.get("contexts")
    par=context[0].get("parameters")
    if action=="troubleshooting.webhook" :
   	    resolution=troubleshoot(par)
    if action=="healthcheck" :
        resolution=healthcheck(par)
    if action=="workinfo.creation" :
        resolution=workinfo(par)
    if action=="predictiveanalysis" :
        resolution=predictiveanalysis(par)
    print(resolution)
    op={'SESSIONID':sessionId,
        'TIME':req.get("timestamp"),
        'ACTION':action,
        'PARAMETERS':par,
        'RESOLUTION':resolution
        }
          
        
'''        print(op)
        session = client.session()
        db = client['jarvis-interaction']
        doc= db.create_document(op)
        doc.save()
        print(doc)'''      
    response="resolution success"
    print(response)
    #except:
        #response="Sorry Bot has faced an issue! Please try after sometime!"
    
    res= {"speech": response,"displayText":response,"source": "jarvis-chatbot"}
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
def troubleshoot(par):
    return "Troubleshooting"
def healthcheck(par):
    return "Healthcheck"
def workinfo(par):    
    return "workinfo"
def predictiveanalysis(par):
    return "Predictive analysis"

def generate_docx(query_res):
    document = Document("static/template.docx")      
    for doc in query_res:
        document.add_heading("CRQ",level=2)
        document.add_paragraph("SERVER:" + doc['SERVER'])
        #document.add_paragraph("Queue MANAGER:" + doc['QMGR'])
    time.sleep(1)
    document.add_paragraph("")    
    document.add_paragraph("© Walgreens")
    document.save("static/workinfo.docx")
    return document

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
       	app.run(host='0.0.0.0', port=int(port), use_reloader=True, debug=True)
