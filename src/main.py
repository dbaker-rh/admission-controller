#!/usr/bin/env python3

from flask import Flask, request, Response, json
# import json

app = Flask(__name__)


@app.route('/')
@app.route('/ping')
@app.route('/healthz')
def root():
    return "OK"


#
# Proof of Concept only
#
# This should verify the request *is* an AdmissionReview
# and ensure all required data fields are present before attempting
# to read them.
#

@app.route('/webhook', methods=['POST'])
def webhook():
    # debug
    print (request.json)

    # Default to failure
    allowed = False

    # Namespace begins with foo?
    if (request.json['request']['spec']['namespace'][0:3] == "foo"): 
      allowed = True


    # ... other processing may take place here ...


    # Create minimal response object
    # - https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response

    response = { "apiVersion": request.json['apiVersion'], "kind": "AdmissionReview", "response": { "uid": request.json['request']['uid'], "allowed": allowed } }

    return json.dumps(response)

    print ("...")
    print (request.json['apiVersion'])
    print (request.json['spec']['namespace'])

    return Response(status=200)




# Future - this service can run multiple webhooks
# to follow is an example of a mutating webhook

@app.route('/mutate', methods=['POST'])
def mutate():
    print(request.json)
    return Response(status=200)


