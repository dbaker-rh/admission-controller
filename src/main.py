#!/usr/bin/env python3

#
#        ###  Proof of Concept only  ###
#
# This code is proof of concept only, and is in no
# way suitable for use in a production environment
#
#
#

from flask import Flask, request, Response, json
from datetime import datetime


app = Flask(__name__)

@app.route('/')
@app.route('/ping')
@app.route('/healthz')
def root():
    return "OK"


#
# Simple validating webhook
#
# - only accept the request if the namespace begins with "foo"
# - corresponding admission controller object must be configured to
#   pass the appropriate requests to this handler
#


@app.route('/webhook', methods=['POST'])
def webhook():
    # debug
    print (request.json)

    # Default to failure
    allowed = False

    # Namespace begins with foo?
    if (request.json['request']['namespace'][0:3] == "foo"): 
      allowed = True


    # ... other processing may take place here ...

    # Create minimal response object
    # - https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response

    response = { "apiVersion": request.json['apiVersion'], "kind": "AdmissionReview", "response": { "uid": request.json['request']['uid'], "allowed": allowed } }
    return json.dumps(response)




#
# Just log requests for diagnostics
#

@app.route('/admissionlogger', methods=['POST'])
def admissionlogger():
    # debug
    print ("[DEBUG] : ", datetime.now())
    print (request.json)

    # Create minimal response object
    # - https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response
    try:
      api = request.json['apiVersion']
    except:
      print ("[DEBUG] : invalid apiVersion in request")
      api = "unknown"

    try:
      uid = request.json['request']['uid']
    except:
      print ("[DEBUG] : invalid uid in request")
      uid = "unknown"

    response = { "apiVersion": api, "kind": "AdmissionReview", "response": { "uid": uid, "allowed": True } }
    return json.dumps(response)





#
# Mutating Webhook
#
# - flip imagePullPolicy to Always
# 
# -- EXCEPT: if namespace is "^openshift(-.*)?$"
#

@app.route('/imagePull-ns', methods=['POST'])
def imagepullns():
    print(request.json)
    return Response(status=200)



#
# Mutating Webhook
#
# - flip imagePullPolicy to Always
#
# -- EXCEPT: if calling user is kubeadmin
#



#
# Mutating Webhook
#
# - flip imagePullPolicy to Always
#
# -- EXCEPT: for given registries
#


