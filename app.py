from __future__ import print_function
from future.standard_library import install_aliases

install_aliases()

import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = ProcessRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# construct search query from result.parameters
def ProcessRequest(req):
    if req.get("result").get("action") != "Maths":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    value1 = parameters.get("number")
    value2 = parameters.get("number1")

    sum = int(value1) + int(value2)
    res = "The sum of two number is: " + str(sum)
    return {
        "speech": res,
        "displayText": res,
        "source": "Athena"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

