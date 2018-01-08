import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request: ")
    print(json.dumps(req, indent=4))
    res = MakeWebRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def MakeWebRequest(req):
    if req.get("request").get("action") != "interest":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    names = parameters.get("org-name")
    organization = {'org1': '10', 'org2': '20', 'org3': '30'}
    speech = "The organization's of " + names + " small projects are: " + str(organization[names])
    print("Response: ")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        "source": "Athena"
    }


if __name__ == '__main__':
    port = int(os.getenv('POST', 5000))
    print("Starting app on %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')


