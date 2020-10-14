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
import base64


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
    print ("[DEBUG] : [RECEIVED] :", datetime.now())
    print (request.json)

    try:
      kind = request.json['kind']
    except:
      print ("[DEBUG] : invalid kind in request")
      kind = "unknown"

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

    response = { "apiVersion": api, "kind": kind, "response": { "uid": uid, "allowed": True } }

    print ()
    print ("[DEBUG] : [RETURNED] :", datetime.now())
    print (json.dumps(response))
    print ()
    return json.dumps(response)





#
# Mutating Webhook
#
# - flip imagePullPolicy to Always
# 
# -- EXCEPT: if namespace is "^openshift(-.*)?$"
#

@app.route('/imagepullon', methods=['POST'])
def imagepullon():
    # debug
    print ("[DEBUG] : [RECEIVED] :", datetime.now())
    print (request.json)

    # Create minimal response object
    # - https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response
    try:
      kind = request.json['kind']
    except:
      print ("[DEBUG] : invalid kind in request")
      kind = "unknown"

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

    dopatch = False;


    ## TODO: don't patch if namespace= .. or user= ..

    try:
      # count how many containers in /request/object/spec/containers ... for each, add the patch 
      # this just sets a patch to edit all of them regardless; we could look at the object to see
      # which, if any, needed to be adjusted to avoid sending a "no-op"
      npod = len( request.json['request']['object']['spec']['containers'] )

      dopatch = True;
      patch = '[ { "op": "replace", "path": "/spec/containers/0/imagePullPolicy", "value": "Always" }'
      for x in range (1, npod):
          patch += ', { "op": "replace", "path": "/spec/containers/' + str(x) + '/imagePullPolicy", "value": "Always" } '
      patch += ']'

      print ()
      print ("[DEBUG] : [PATCH]")
      print (patch)
    except:
      print ()
      print ("[DEBUG] : No containers found in request")


    # flip string to bytes and back
    if (dopatch):
      response = { "apiVersion": api, "kind": kind, "response": { "uid": uid, "allowed": True, "patchType": "JSONPatch", "patch": base64.b64encode(patch.encode()).decode() } }
    else:
      response = { "apiVersion": api, "kind": kind, "response": { "uid": uid, "allowed": True } }


    print ()
    print ("[DEBUG] : [RETURNED] :", datetime.now())
    print (json.dumps(response))
    print ()
    return json.dumps(response)
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


