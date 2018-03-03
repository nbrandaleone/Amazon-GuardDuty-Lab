import boto3
import botocore
import json
 
 
APPLICABLE_APIS = ["aws.guardduty"]
def evaluate_compliance(event):
    #print(event["source"])
    #try:
    event_name = event["source"]
    print event["source"]
    if event_name not in APPLICABLE_APIS:
        print("This rule does not apply for the event ", event_name, ".")
        return
    else:
        ParserCore(event)
        #except:
        #    print("Fail")
        #    return
 
def ParserCore(event):
    client = boto3.client('lambda')
    print event["detail"]["service"]["additionalInfo"]["threatName"]
    #print event["service"]
    if event["detail"]["service"]["additionalInfo"]["threatName"] == "Customer Threat Intel":
       print "Kicking off forensics"
       response = client.invoke_async(
            FunctionName='CloudWatcher_Authorize_SecurityGroupChange',
            InvokeArgs=bytes(json.dumps(event))
        )
       print response
    else:
        print "Not currently a Coded Issue"
        print event["eventName"]
 
def lambda_handler(event, context):
    #print("event: ", json.dumps(event))
    evaluation = evaluate_compliance(event)