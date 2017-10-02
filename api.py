from base64 import decodestring
import json
import jsonschema
from jsonschema import validate
from flask import Flask, request, jsonify

app = Flask(__name__)

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
  
  with open("imageToSave.png", "wb") as fh:
    fh.write(decodestring(data["b"][0]))

  return "ok", 200

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080)
