import boto3
import json

ec2_client = boto3.client('ec2', region_name='us-east-1')
""":type: pyboto3.ec2"""

response = ec2_client.describe_instances()

for res in response['Reservations']:
    for inst in res['Instances']:
        print(inst['PublicIpAddress'])