import boto3

TOPIC_NAME = 'SubTopic'
TOPIC_ARN = 'arn:aws:sns:us-east-1:463148421511:SubTopic'
QUEUE_ARN = 'arn:aws:sqs:us-east-1:835152019027:MainQ'


def sns_client():
    sns = boto3.client('sns', region_name='us-east-1')
    """ :type: pyboto3.sns"""
    return sns


def create_topic():
    return sns_client().create_topic(
        Name=TOPIC_NAME
    )


def get_topics():
    return sns_client().list_topics(
    )


def get_topic_attrs():
    return sns_client().get_topic_attributes(
        TopicArn=TOPIC_ARN
    )


def update_topic_attrs():
    return sns_client().set_topic_attributes(
        TopicArn=TOPIC_ARN,
        AttributeName='DisplayName',
        AttributeValue='Sample SNS topic'
    )


def delete_topic():
    return sns_client().delete_topic(
        TopicArn=TOPIC_ARN
    )


def create_email_sub(topic_arn, email_addrs):
    return sns_client().subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email_addrs
    )


def create_sms_sub(topic_arn):
    return sns_client().subscribe(
        TopicArn=topic_arn,
        Protocol='sms',
        Endpoint='+919686570774'
    )


def create_sqs_sub(topic_arn, queue_arn):
    return sns_client().subscribe(
        TopicArn=topic_arn,
        Protocol='sqs',
        Endpoint=queue_arn
    )

def get_topics_sub(topic_arn):
    return sns_client().list_subscriptions_by_topic(
        TopicArn=topic_arn
    )

def list_opted_out_phns():
    return sns_client().list_phone_numbers_opted_out()

def email_opt_out(email_addrs):
    subs = get_topics_sub(topic_arn)


if __name__ == '__main__':
    # Run code here
    # create_topic()
    # print(get_topics())
    # print(get_topic_attrs())
    # print(delete_topic())
    # print(create_email_sub(TOPIC_ARN, 'pgandla.aws@gmail.com'))
    # create_sms_sub(TOPIC_ARN)
    # create_sqs_sub(TOPIC_ARN, QUEUE_ARN)
    # print(get_topics_sub(TOPIC_ARN))
    print(list_opted_out_phns())