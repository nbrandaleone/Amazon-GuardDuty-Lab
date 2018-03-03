import boto3
from botocore.exceptions import ClientError
 
 
def lambda_handler(event, context):
    #print("event: ", json.dumps(event))
    try:
        ec2 = boto3.client('ec2')
        name = 'Forensics' + event["detail"]["id"]
        response = ec2.describe_vpcs()
        vpc_id = event["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["vpcId"]
        instanceID = event["detail"]["resource"]["instanceDetails"]["instanceId"]
        print instanceID
    
        
        response = ec2.create_security_group(GroupName=name,
                 Description='This is a closed dead zone for testing of a breached system in the defulat VPC',
                 VpcId=vpc_id)
        print  response 
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
       
        ec2 = boto3.resource('ec2')
        filters = {"Name":"instance-id","Values":instanceID}
        print filters
        #instances = ec2.instances.filter(Filters=filters)
        instance = ec2.Instance(instanceID)
        #for instance in instances:
        print(instance.id, instance.instance_type)
        all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]  # Get a list of ids of all securify groups attached to the instance
        print all_sg_ids
        for sg_id in all_sg_ids:                                          # Check the SG to be removed is in the list
            print sg_id
            all_sg_ids.remove(sg_id)                                       # Remove the SG from the list
            instance.modify_attribute(Groups=[security_group_id])                   # Attach the remaining SGs to the instance
               
                
    except ClientError as e:
        print(e)