import boto3
import os
import json
import datetime
from botocore.exceptions import ClientError

org_client = boto3.client('organizations')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

ASSUME_ROLE_NAME = 'RootComplianceAuditRole'

def lambda_handler(event, context):
    accounts = get_accounts()
    timestamp = datetime.datetime.utcnow().isoformat()

    for account in accounts:
        session = assume_role(account['Id'])
        if not session:
            continue

        iam_client = session.client('iam')
        result = {
            'AccountId': account['Id'],
            'AccountName': account['Name'],
            'Timestamp': timestamp,
            'RootMFAEnabled': None,
            'RootAccessKeysPresent': None
        }

        # Check root MFA
        try:
            summary = iam_client.get_account_summary()
            mfa_enabled = summary['SummaryMap'].get('AccountMFAEnabled', 0)
            result['RootMFAEnabled'] = bool(mfa_enabled)
        except ClientError as e:
            print(f"[ERROR] MFA check error in {account['Id']}: {e}")

        # Check root access keys
        try:
            access_keys = iam_client.list_access_keys(UserName='root')
            result['RootAccessKeysPresent'] = bool(access_keys['AccessKeyMetadata'])
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                result['RootAccessKeysPresent'] = False
            else:
                print(f"[ERROR] Access keys check error in {account['Id']}: {e}")

        # Store result
        table.put_item(Item=result)
        print(f"[INFO] Recorded: {result}")

    return {
        'statusCode': 200,
        'body': json.dumps('Audit completed')
    }

def get_accounts():
    accounts = []
    paginator = org_client.get_paginator('list_accounts')
    for page in paginator.paginate():
        for acct in page['Accounts']:
            if acct['Status'] == 'ACTIVE':
                accounts.append({
                    'Id': acct['Id'],
                    'Name': acct['Name']
                })
    return accounts

def assume_role(account_id):
    sts_client = boto3.client('sts')
    role_arn = f'arn:aws:iam::{account_id}:role/{ASSUME_ROLE_NAME}'
    try:
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName='RootComplianceAudit'
        )
        credentials = response['Credentials']
        return boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
    except ClientError as e:
        print(f"[ERROR] Could not assume role in {account_id}: {e}")
        return None
