import boto3
import json

Queue_Name = 'MyTest-Sqs'
QueueUrl = 'https://queue.amazonaws.com/789377360425/MyTest-Sqs'
fifoQueue = 'MyTestQ.fifo'
FifoQ = 'https://queue.amazonaws.com/789377360425/MyTestQ.fifo'
DeadLetterQ = 'DeadLetterQ'
MainQ = "MainQ"
MainQUrl = 'https://queue.amazonaws.com/789377360425/MainQ'


def sqs_client():
    sqs = boto3.client('sqs', region_name='us-east-1')
    """ :type: pyboto3.sqs"""
    return sqs


def create_sqs_queue():
    return sqs_client().create_queue(
        QueueName=Queue_Name
    )


def create_fifo_queue():
    return sqs_client().create_queue(
        QueueName=fifoQueue,
        Attributes={
            'FifoQueue': 'true'
        }
    )


def create_dead_letter_queue():
    return sqs_client().create_queue(
        QueueName=DeadLetterQ
    )


def create_main_queue():
    redrive_policy = {
        "deadLetterTargetArn": "arn:aws:sqs:us-east-1:789377360425:DeadLetterQ",
        "maxReceiveCount": 3
    }
    return sqs_client().create_queue(
        QueueName=MainQ,
        Attributes={
            "DelaySeconds": "0",
            "MaximumMessageSize": "262144",
            "VisibilityTimeout": "30",
            "MessageRetentionPeriod": "345680",
            "ReceiveMessageWaitTimeSeconds": "0",
            "RedrivePolicy": json.dumps(redrive_policy)
        }
    )


def find_queue():
    return sqs_client().list_queues(
        QueueNamePrefix='MyTest'
    )


def list_all_queues():
    return sqs_client().list_queues()


def get_queue_attr():
    return sqs_client().get_queue_attributes(
        QueueUrl=MainQUrl,
        AttributeNames=['MaximumMessageSize', 'VisibilityTimeout']
    )


def update_queue_attrs():
    return sqs_client().set_queue_attributes(
        QueueUrl=MainQUrl,
        Attributes={
            'MaximumMessageSize': "131072",
            "VisibilityTimeout": "15"
        }
    )


def delete_queue():
    return sqs_client().delete_queue(
        QueueUrl=QueueUrl
    )


def send_message_queue():
    return sqs_client().send_message(
        QueueUrl=MainQUrl,
        MessageAttributes={
            'Title': {
                'DataType': "String",
                "StringValue": "My SQS Mess"
            },
            'Author': {
                'DataType': "String",
                'StringValue': "Pradeep"
            },
            'Time': {
                'DataType': "Number",
                "StringValue": "6"
            }
        },
        MessageBody='This is my first SQS message'
    )


def send_batch_messages():
    return sqs_client().send_message_batch(
        QueueUrl=MainQUrl,
        Entries=[
            {
                'Id': '1',
                'MessageBody': 'This is 1 Message'
            },
            {
                'Id': '2',
                'MessageBody': 'This is 2 Message'
            },
            {
                'Id': '3',
                'MessageBody': 'This is 3 Message'
            },
            {
                'Id': '4',
                'MessageBody': 'This is 4 Message'
            }
        ]
    )


def poll_queue_message():
    return sqs_client().receive_message(
        QueueUrl=MainQUrl,
        MaxNumberOfMessages=10
    )


def change_visibility_timeout(receipt_handle):
    sqs_client().change_message_visibility(
        QueueUrl=MainQUrl,
        ReceiptHandle=receipt_handle,
        VisibilityTimeout=5
    )


def process_message_queue():
    queued_messages = poll_queue_message()
    if 'Messages' in queued_messages and len(queued_messages['Messages']) >= 1:
        for message in queued_messages['Messages']:
            print('Processing message ' + message['MessageId'] + ' message name ' + message['Body'])
            # delete_message_queue(message['ReceiptHandle'])
            change_visibility_timeout(message['ReceiptHandle'])

def delete_message_queue(receipt_handle):
    return sqs_client().delete_message(
        QueueUrl=MainQUrl,
        ReceiptHandle=receipt_handle
    )

def purge_queue():
    return sqs_client().purge_queue(
        QueueUrl=MainQUrl
    )

if __name__ == '__main__':
    # print(create_sqs_queue())
    # print(create_fifo_queue())
    # create_dead_letter_queue()
    # print(create_main_queue())
    # print(find_queue())
    # print(list_all_queues())
    # update_queue_attrs()
    # print(get_queue_attr())
    # print(delete_queue())
    # print(send_message_queue())
    # print(send_batch_messages())
    # print(poll_queue_message())
    # process_message_queue()
    purge_queue()