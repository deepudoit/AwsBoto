import boto3
import os


def lambda_handler(event, context):
    try:
        vpc_id = event['detail']['responseElements']['vpc']['vpcId']
        print('vpc_id', vpc_id)
        ec2_client = boto3.client('ec2')
        """ :type: pyboto3.ec2"""

        response = ec2_client.describe_flow_logs(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [
                        vpc_id
                    ]
                }
            ]
        )

        if len(response[u'FlowLogs']) != 0:
            print('VPC flow logs are enabled')
        else:
            print('VPC Flow logs are disabled')
            print('Flowlogs grp name; ' + os.environ['FLOWGRP_NAME'])
            print('ROLE_ARN: ' + os.environ['ROLE_ARN'])

            response = ec2_client.create_flow_logs(
                ResourceIds=[vpc_id],
                ResourceType='VPC',
                TrafficType='ALL',
                LogGroupName=os.environ['FLOWGRP_NAME'],
                DeliverLogsPermissionArn=os.environ['ROLE_ARN']
            )

            print('Created Flow: ' + response['FlowLogIds'][0])

    except Exception as ex:
        print('Error  : "%s"' % str(ex))

