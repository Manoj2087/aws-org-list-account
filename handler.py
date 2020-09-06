import csv
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

# Env Var
accountS3Bucket = os.environ['ACCOUNTS3BUCKET']
accountsPath = os.environ['ACCOUNTSPATH']
# Global Var
accountList = [['cust_account_id','cust_account_name','cust_account_status']]

def listAccounts():
    """Fetchs the Linked AWS Accounts"""
    try:
        global accountList
        client = boto3.client('organizations')
        paginator = client.get_paginator('list_accounts')
        page_iterator = paginator.paginate(PaginationConfig={'PageSize': 20})
        for page in page_iterator:
            # print(page['Accounts'])
            for account in page['Accounts']:
                # print((account['JoinedTimestamp']))
                # print(account['JoinedTimestamp'].strftime('%Y-%m-%d %H:%M:%S.000'))
                item = [account['Id'],account['Name'],account['Status']]
                accountList.append(item)
    except Exception as e:
        raise e
          
def uploadToS3(tmpOutFilePath, key):
    """docstring for uploadToS3"""
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(accountS3Bucket)
        bucket.upload_file(tmpOutFilePath, key, ExtraArgs={'ACL': 'bucket-owner-full-control'})
    except Exception as e:
        raise e

def main(event, context):
    try:
        global accountList
        tmpOutFilePath = '/tmp/output.csv'
        listAccounts()
        print(accountList)
        with open(tmpOutFilePath, 'w', newline='') as result_file:
            wr = csv.writer(result_file)
            wr.writerows(accountList)
        key = accountsPath + '/accounts.csv'
        uploadToS3(tmpOutFilePath, key)
        # Clean up
        os.remove(tmpOutFilePath)
        accountList = []
        response = {
            'statusCode': 200,
            'body': 'Execution complete. Check CloudWatch Logs for execution detail'
        }
        return response

    except Exception as e:
        raise e