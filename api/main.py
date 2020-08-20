#-------------------------------------------------------------
 # 
 #   .SYNOPSIS
 #   API endpoint for MarketPntl.
 #   
 #   .NOTES
 #   Author: Charles Christensen
 #   Required Dependencies: flask, request, marketpntl
 #   
#-------------------------------------------------------------

#==========================================
#  PARMETERS / VARIABLES
#==========================================

# Decompressed added binaries.
try:
    import unzip_requirements
except ImportError:
    pass

# Initialize genuine libraries.
from flask import Flask, render_template, request
from flask_cors import CORS
import boto3
import json

# Initialize in-house development.
import marketpntl

#==========================================
#  FUNCTIONS
#==========================================

# Create a JSON response.
def makeJsonResponse(int(status), data):
    if status == 1:
        data = {
            "message": "Success",
            "result": data
        }
    elif status == -1:
        data = {
            "message": "Busy",
            "result": data
        }    
    else:
        data = {
            "message": "Error",
            "result": data
        }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    
    return response

# Verify HS code.
def verifyHs(raw_hs):
    hs = 0
    try:
        hs = int(raw_hs)
    except:
        return False
    
    if (len(str(raw_hs)) == 6):
        return True
    else:
        return False

#==========================================
#  MAIN
#==========================================

# Begin Flask.
app = Flask(__name__)
CORS(app)

# Define routes.
@app.route('/', methods = ['GET','POST'])
def default():
    return makeJsonResponse(False, "Invalid API request.")

@app.route('/marketpntl/data', methods = ['POST'])
def marketpntl_data_in():
    
    # Validate request.
    hs = request.get_json(force=True).get('hs')
    if not verifyHs(hs):
        return makeJsonResponse(False, "Invalid HS code.")
    
    # Execute request.
    #results = marketpntl.pull_all_data(hs)
    #DEBUG: add something here to kick other lambda function into running
    
    return makeJsonResponse(True, "HS data is being collected.")
    
@app.route('/marketpntl/data/<hs>', methods = ['GET'])
def marketpntl_data_out(hs):

    # Connect to S3.
    s3 = boto3.resource('s3')

    # Check for results being complete.
    #DEBUG: add something here to look for HS#.json is S3.
    
    # Check for possible errors.
    #DEBUG: add something here to check error.json for corresponding error.
    #return makeJsonResponse(False, error_msg)
    
    # Send still processing message.
    return makeJsonResponse(-1, "Data still processing.")

@app.route('/marketpntl/results', methods = ['POST'])
def marketpntl_results():
    
    # Validate request.
    data = request.get_json(force=True).get('data')
    main_weights = request.get_json().get('main_weights')
    sub_weights = request.get_json().get('sub_weights')
    
    # Execute request.
    results = marketpntl.analyze_all_data(data, main_weights, sub_weights)
    return makeJsonResponse(not(isinstance(results, str)), results)

# Start Flask server.
if __name__ == "__main__":
    app.run(host="0.0.0.0")
