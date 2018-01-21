import cv2
import itertools
import os
import sys
import logging

import numpy as np
np.set_printoptions(precision=2)

import openface

from base64 import decodestring
import json
import jsonschema
from jsonschema import validate
from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
#db = MongoClient('localhost', 27017).hodor

schema = {
  "type" : "object",
    "properties" : {
      "a": {
        "type" : "object",
        "minProperties": 2,
        "additionalProperties": {
          "type": "string"
        }
      },
      "b": {
        "type" : "array",
        "items": {
          "type": "string",
          "minLength": 1
        },
        "minItems": 1
      }
    },
    "required": [
      "a",
      "b"
    ]
}

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '.', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

align = openface.AlignDlib(os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
net = openface.TorchNeuralNet(os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'), 96)

def getRep(imgBase64):    
    nparr = np.fromstring(decodestring(imgBase64), np.uint8)
    bgrImg = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if bgrImg is None:
        raise Exception("Unable to load image")

    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
    bb = align.getLargestFaceBoundingBox(rgbImg)

    if bb is None:
        raise Exception("Unable to find a face")

    alignedFace = align.align(96, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image")

    return net.forward(alignedFace)

@app.route('/compare', methods=['POST'])
def compare():
  data = request.get_json()
  try:
    validate(data, schema)
  except jsonschema.exceptions.ValidationError as ve:
    return jsonify({  
      'message' : ve.message, 
      'path' : '.'.join(ve.absolute_schema_path) 
    }), 400
  except Exception as e: 
    return e.message, 400 

  imgs = []
  errs = []

  for imgBase64 in data['b']:
    try:
      imgs.append(getRep(imgBase64))
    except Exception as e:
      errs.append(e.message)
  
  for user, imgBase64 in data['a'].iteritems():
    try:
      rep = getRep(imgBase64)
      d = rep - imgs[0]
      data['a'][user] = "{:0.3f}".format(np.dot(d, d))
    except Exception as e:
      errs.append(e.message)
      print(e.message)

  return jsonify(data['a']), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
