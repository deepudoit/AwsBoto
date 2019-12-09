import os


def lambda_handler(event, context):
    # return {
    #     'statuscode': 200,
    #     'message': 'Hello from python lambda fn'
    # }
    env_var = os.getenv('ENV_VAR_TEST')
    return {
        'statusCode': 200,
        'message': env_var
    }