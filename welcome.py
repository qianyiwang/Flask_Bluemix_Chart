# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, render_template, request, json
from datetime import datetime
import pygal

global data, time
data = []
time = []

app = Flask(__name__)

@app.route('/')
def Welcome():
    global data, time
    print data, time
    print "Welcome ... "
    try:
        graph = pygal.Line()
        graph.title = "% Data Received"
        graph.x_labels = time
        graph.add('Data', data)
    
        graph_data = graph.render_data_uri()
        return render_template('graphing.html', graph_data=graph_data)
    except Exception, e:
        return(str(e))

@app.route('/receiveData/', methods = ['POST', 'GET'])
def receiveData():
    global data
    jsondata = request.get_json()
    d = json.loads(jsondata)['Data']
    data.append(int(d))
    time.append(str(datetime.now()))
    print data, time
    result = {'escalate': True}
    return json.dumps(result)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), )
