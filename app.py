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
    if req.get("queryResult").get("action") != "Maths":
        return {}
    json_params = req.get("queryResult").get("queryText")
    take = json_params.split()

    sum = 0

    if take[1] == '+':
        sum = int(take[0] + '') + int(take[2] + '')
        # print(sum)

    if take[1] == '-':
        sum = int(take[0] + '') - int(take[2] + '')
        # print(sum)

    if take[1] == '*':
        sum = int(take[0] + '') * int(take[2] + '')
        # print(sum)

    if take[1] == '/':
        if int(take[2]) != 0:
            sum = int(take[0] + '') / int(take[2] + '')
            # print(sum)
        else:
            return "Invalid"

    res = sum
    return {
        "displayText": str(res),
        # "data": {},
        # "contextOut": [],
        "source": "cramstack-backend"
        
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
