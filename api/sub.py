#-------------------------------------------------------------
 # 
 #   .SYNOPSIS
 #   API background process for MarketPntl.
 #   
 #   .NOTES
 #   Author: Charles Christensen
 #   Required Dependencies: request, marketpntl
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
import json
import boto3

# Initialize in-house development.
import marketpntl

#==========================================
#  MAIN
#==========================================

def handler(event, context):
    
    # Launch data fetch.
    hs = event['Records'][0]['Sns']['Message']['hs']
    results = marketpntl.pull_all_data(hs)
    
    # Connect to S3.
    s3 = boto3.resource('s3')
    
    # Do not execute if data is already present.
    try:
        s3.Object('marketpntl-data', hs + ".json").load()
    except:
        
        # Save and/or report results.
        if isinstance(results, str):
            #DEBUG: Add save to error file
            return results
        
        else:
            #DEBUG: add save to S3 bucket
            return "Data fetch complete."
        
    else:
        reture "Data fetch complete."