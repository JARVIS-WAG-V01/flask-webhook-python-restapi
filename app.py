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
    try:
        req=request.get_json(silent=True,force=True)
        sessionId=req.get("sessionId")
        result=req.get("result")
        action=result.get("action")
        par=result.get("contexts").get("parameters")
        if action=="troubleshooting.webhook" :
       	    result=troubleshoot(par)
        if action=="healthcheck" :
            result=healthcheck(par)
        if action=="workinfo.creation" :
            result=workinfo(par)
        if action=="predictiveanalysis" :
            result=predictiveanalysis(par)
        
        op={'SESSIONID':sessionId,
            'TIME':req.get("timestamp"),
            'ACTION':action,
            'PARAMETERS':par,
            'RESOLUTION':result
            }
           
        
        print(op)
        session = client.session()
        db = client['jarvis-interaction']
        doc= db.create_document(op)
        doc.save()
        print(doc)
        #send_data=requests.post(url,data={'key':weightage,'sessionId':sessionId})
       
        response=result
    #except:
        response="Sorry Bot has faced an issue! Please try after sometime!"
    
    res= {"speech": response,"displayText": "******","source": "nWave-estimation-chatbot"}
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



port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
       	app.run(host='0.0.0.0', port=int(port), use_reloader=True, debug=True)
