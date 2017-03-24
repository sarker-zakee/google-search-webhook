# A Google Search Webhook Implementation in Python

This is a really simple webhook implementation that gets Api.ai classification JSON (i.e. a JSON output of Api.ai /query endpoint) and returns a fulfillment response.

# Deploy to:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# What does the service do?
It's a google search fulfillment service that uses [Custom Search API](https://developers.google.com/custom-search/).
The service takes parameters from the action and requests a more abstract search based on the user's initial naive question from Google's Custom Search API. 

The service returns the result in the Api.ai webhook-compatible response JSON to Api.ai chatbot.
