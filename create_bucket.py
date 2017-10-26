#!usr/bin/env python3

import boto3
import json
from random import *


def create_s3_bucket():
    s3 = boto3.client('s3')

    try:
        bucket_number = randint(0, 1000)
        bucket_name = 'my-unique-bucket-' + str(bucket_number)  # Each bucket name must be wholly unique
        s3.create_bucket(
            ACL='public-read',  # Grants read access to all users
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-west-1',  # Makes sure bucket created in same region as ec2 instance
            }
        )

        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': 'arn:aws:s3:::' + bucket_name + '/*'

            }]
        }

        bucket_policy = json.dumps(bucket_policy)
        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=bucket_policy
        )

        print('A new s3 bucket has been created:', bucket_name)

    except Exception as err:
        print(err)


def main():
    create_s3_bucket()


if __name__ == '__main__':
    main()