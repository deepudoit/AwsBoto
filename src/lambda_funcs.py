import boto3
import json
from os import path
from src.Utils import Utils

LAMBDA_ROLE = "Lambda_Exe_Role"
POLICY_ARN = "arn:aws:iam::013540878537:policy/LambdaS3Policy"
LAMBDA_ROLE_ARN = "arn:aws:iam::013540878537:role/Lambda_Exe_Role"
LAMBDA_TIMEOUT = 10
LAMBDA_MEM = 128
LAMBDA_HANDLER = 'lambda_fn.lambda_handler'
PYTHON_37_RUNTIME = 'python3.7'
NODEJS_10_RUNTIME = "nodejs10.x"
LAMBDA_NAME = 'LambdaNodeJS'


def lambda_client():
    aws_lambda = boto3.client('lambda', region_name='us-east-1')
    """ :type: pyboto3.lambda_"""
    return aws_lambda


def iam_client():
    iam = boto3.client('iam')
    """ :type: pyboto3.iam"""
    return iam


def create_access_policy_lambda():
    s3_access_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:*",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "*"
            }
        ]
    }
    return iam_client().create_policy(
        PolicyName="LambdaS3Policy",
        PolicyDocument=json.dumps(s3_access_policy),
        Description="Lambda S3 access policy"
    )


def create_lambda_role():
    lambda_role = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    return iam_client().create_role(
        RoleName=LAMBDA_ROLE,
        AssumeRolePolicyDocument=json.dumps(lambda_role),
        Description="Lambda execution role"
    )


def attach_accesspolicy_role():
    return iam_client().attach_role_policy(
        RoleName=LAMBDA_ROLE,
        PolicyArn=POLICY_ARN
    )


def deploy_lambda_fn(fn_name, run_time, handler, role_arn, src_folder):
    folder_path = path.join(path.dirname(path.abspath(__file__)), src_folder)
    zip_file = Utils.make_zip_filebytes(path=folder_path)
    return lambda_client().create_function(
        FunctionName=fn_name,
        Runtime=run_time,
        Role=role_arn,
        Handler=handler,
        Code={
            'ZipFile': zip_file
        },
        Timeout=LAMBDA_TIMEOUT,
        MemorySize=LAMBDA_MEM,
        Publish=False
    )


def invoke_func(func_name):
    return lambda_client().invoke(
        FunctionName=func_name
    )


def add_env_lambda(func_name, vars):
    return lambda_client().update_function_configuration(
        FunctionName=func_name,
        Environment=vars
    )


def update_lambda_code(func_name, src_folder):
    folder_path = path.join(path.dirname(path.abspath(__file__)), src_folder)
    zip_file = Utils.make_zip_filebytes(path=folder_path)
    return lambda_client().update_function_code(
        FunctionName=func_name,
        ZipFile=zip_file
    )


def publish_lambda_fn(func_name):
    return lambda_client().publish_version(
        FunctionName=func_name
    )


def create_alias_version(func_name, alias_name, version):
    return lambda_client().create_alias(
        FunctionName=func_name,
        Name=alias_name,
        FunctionVersion=version,
        Description='This is PROD version'
    )


if __name__ == '__main__':
    # print(create_access_policy_lambda())
    # print(create_lambda_role())
    # print(attach_accesspolicy_role())
    # print(deploy_lambda_fn(LAMBDA_NAME, PYTHON_37_RUNTIME, LAMBDA_HANDLER, LAMBDA_ROLE_ARN, 'python_lambda'))
    # print((deploy_lambda_fn(LAMBDA_NAME, NODEJS_10_RUNTIME, LAMBDA_HANDLER, LAMBDA_ROLE_ARN, 'nodejs_lambda')))
    # response = invoke_func(LAMBDA_NAME)
    # print(response['Payload'].read().decode())
    # env_var = {
    #     'Variables': {
    #         'ENV_VAR_TEST': 'This is an env var'
    #     }
    # }
    # add_env_lambda(LAMBDA_NAME, env_var)
    # update_lambda_code(LAMBDA_NAME, 'python_lambda')
    # response = invoke_func(LAMBDA_NAME)
    # print(response['Payload'].read().decode())
    # print(publish_lambda_fn(LAMBDA_NAME))
    print(create_alias_version(LAMBDA_NAME, 'PROD', '1'))