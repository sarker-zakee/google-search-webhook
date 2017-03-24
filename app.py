#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

from googleapiclient.discovery import build
import pprint

# Flask app should start in global layout
app = Flask(__name__)

my_api_key = "AIzaSyBdAw3e3wCRd9KIds9yMqQUvqM8BjmH1io"
my_cse_id = "003838730819932693587:t35aahzuprq"
searchString = ""

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# construct search query from result.parameters
def processRequest(req):
    # if req.get("result").get("action") != "googleSearch":
    #     return {}
    # baseurl = "https://query.yahooapis.com/v1/public/yql?"
    # yql_query = makeYqlQuery(req)
    # if yql_query is None:
    #     return {}
    # yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    # result = urlopen(yql_url).read()
    # data = json.loads(result)
    # res = makeWebhookResult(data) #takes in api response and returns final json to send back
    # return res
    if req.get("result").get("action") != "googleSearch":
        return {}
    json_params = req.get("result").get("parameters")
    searchstring = "".join(json_params.values())    # this creates the overall topic which covers user's raw query

    searchString = "robot %s site:en.wikipedia.org" % searchstring

    searchResults = google_search(searchString, my_api_key, my_cse_id, num=1)    # search for the topic
    if searchResults is None:
        return{}

    res = makeWebhookResult(searchResults)
    return res


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def makeWebhookResult(data):
    articleUrl = data[0].get('formattedUrl')
    if query is None:
        return {}

    if (data[0] is None):
        return {}

        # print(json.dumps(item, indent=4))

    speech = "Please view this article for more information on " + searchString + ": " \
             articleUrl

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "google-search-webhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
