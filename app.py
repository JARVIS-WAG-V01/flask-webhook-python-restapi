import json
import os
import requests
import pickle
import pandas as pd
import cloudant
from cloudant import Cloudant
from docx import Document
from flask import Flask , request, make_response , render_template, session,g
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey,QueryResult

user= ""
password= ""
host= ""
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
       	    troubleshoot(par)
        if action=="healthcheck" :
            healthcheck(par)
        if action=="workinfo.creation" :
            workinfo(par)
        if action=="predictiveanalysis" :
            predictiveanalysis(par)
        weightage=intRegression(req)
        op={'SESSIONID':sessionId,
            'TIME':req.get("timestamp"),
            'ACTION':action,
            'PARAMETERS':par,
            'RESOLUTION':result.get("fulfillment").get("speech")
            }
            
        
        print(op)
        session = client.session()
        db = client['jarvis-interaction']
        doc= db.create_document(op)
        doc.save()
        print(doc)
        #send_data=requests.post(url,data={'key':weightage,'sessionId':sessionId})
       
        response="*****"
    except:
        response="Sorry Bot has faced an issue! Please try after sometime!"
    
    res= {"speech": response,"displayText": "******","source": "nWave-estimation-chatbot"}
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
   
de*********f intRegression(req):
    #Machine Learning Model
    dataset = pd.read_excel("https://github.com/s-gunalan/nWave-Flask-Demo/blob/master/dataset_integration_v2.xlsx?raw=true",skip_header=1)
    #dataset=pd.read_excel("D:/Guna/POCs/ML/nWave_effort/dataset_integration.xlsx",skip_header=1)
    Y=dataset.iloc[:, 13:]
    X=dataset.iloc[:,1:13]
    header=list(X)
    imputer = Imputer()
    dataset = imputer.fit_transform(X)
    lr=LinearRegression()
    model_int=lr.fit(X,Y)

    #Data Processing
    val=[]
    result=req.get("result")
    contexts=result.get("contexts")
    print(contexts[0])
    parameters=contexts[0].get("parameters")
    for i in header:
        str=parameters.get(i)
        print("%s %s " %(i,str))
        val.append(str)
    ds=pd.DataFrame(val).T
    print(ds)

    #Prediction
    op_lrt=lr.predict(ds)
    op=round(op_lrt[0][0],2)
    print(op)
    return op



port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
       	app.run(host='0.0.0.0', port=int(port), use_reloader=True, debug=True)
