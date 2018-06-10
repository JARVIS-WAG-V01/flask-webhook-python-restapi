import json
import requests
import os
import time
import cloudant
from cloudant import Cloudant
import pandas as pd
from docx import Document
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey, QueryResult
from flask import Flask, request, make_response, render_template, session, g

user= "000d5b69-974a-4f7b-9118-5bcb7aed2484-bluemix"	
password= "ecab228d0b549390a55b708bcfe28f6818e223aa5761dc2628e65859c7211e87"	
host= "000d5b69-974a-4f7b-9118-5bcb7aed2484-bluemix.cloudant.com"
url = 'https://' + host
client = Cloudant(user, password, url=url, connect=True)
app=Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
    req= request.get_json(silent=True, force=True)
    sessionId=req.get("sessionId")
    result=req.get("result")
    contexts=result.get("contexts")
    print(contexts)
    action=result.get("action")
    print(action)
    par=contexts[0].get("parameters")
    resolution = "Incomplete"
    if action == "troubleshooting.webhook" :
        resolution =  troubleshoot(par)
    if action == "healthcheck" :
        resolution = healthcheck(par)
    if action == "workinfo.creation" :
        resolution = workinfo(par)
    if action == "predictiveanalysis" :
        resolution = predictiveanalysis(par)
    if action == "updateproperties.beta" :
        resolution = "update props"
    
    res={"speech":resolution, "displayText":resolution, "source":"jarvis-chatbot"}
    res=json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def troubleshoot(par):
    SERVER = par.get("SERVER")
    APPLICATION = par.get("APPLICATION")
    session = client.session()
    db = client['esb-data']
    query_ts = cloudant.query.Query(db,selector={"SERVER":SERVER,"APPLICATION":APPLICATION})
    time.sleep(1)
    queryresult_ts = QueryResult(query_ts)
    print(queryresult_ts)
    for doc in queryresult_ts:
        try:  
            print(doc['FLOW_NAME'])
        except:
            print(doc['QUEUE'])
    result = SERVER + APPLICATION
    #details={}
    #log=client['jarvis-interaction']
    #doc=log.create_document(details)
    #doc.save()
    return result

def healthcheck(par):
    SERVER= par.get("SERVER")
    result = SERVER
    return result

def workinfo(par):
    SERVER= par.get("SERVER")
    TASK= par.get("WORKINFO-TASK")
    result = SERVER + TASK
    return result
    
def predictiveanalysis(par):
    return "From my analysis "
    
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), use_reloader=True, debug=True)
