#!usr/bin/env python3

import boto3
import time
import subprocess
from random import *


def create_ec2_instance():
    ec2 = boto3.resource('ec2')

    # Creates the ec2 instance with its variables
    instance = ec2.create_instances(
        ImageId='ami-acd005d5',
        MinCount=1,
        MaxCount=1,
        KeyName='BriansKey',
        SecurityGroupIds=['sg-ed51b996'],
        UserData='''#!/bin/bash
                    yum -y update
                    yum -y install python35        
                    yum -y install nginx 
                    service nginx start
                    chkconfig nginx on''',
        InstanceType='t2.micro')

    print('An instance has been created with an ID of: ', instance[0].id)
    time.sleep(5)
    instance[0].reload()
    print('The new instance has a public IP address of:', instance[0].public_ip_address)

    instance[0].create_tags(
        Resources=[instance[0].id],
        Tags=[
            {
                'Key': 'Name', # Calling the Key "Name" ensures it appears on the default view
                'Value': 'Dev_Ops_Assignment'
            },
        ]
    )

    print('The instance ', instance[0].id, ' has been given a new tag')

    ec2_user = 'ec2-user@' + instance[0].public_ip_address
    cmd = "ssh -o StrictHostKeyChecking=no -i BriansKey.pem " + ec2_user + " 'pwd'"
    # Connects to instance via ssh
    #  -o provides options (suppresses the yes/no response from host key confirmation)
    print('\nRunning command:', cmd, '\n')

    time.sleep(60)  # Halts program for 1 minute to allow the instance load before SSH is available
    instance[0].reload()
    (status, output) = subprocess.getstatusoutput(cmd)
    if status == 0:
        print('\nssh into ec2 instance successful', output)
    else:
        print('ssh failed\n')

    scp = 'scp -i BriansKey.pem check_webserver.py ' + ec2_user +':.'
    (status, output) = subprocess.getstatusoutput(scp)
    if status == 0:
        print('\nSuccessfully copied check_webserver.py to ec2 instance'
              '\nGranting executable privilages for check_webserver.py')
        cmd1 = "ssh -i BriansKey.pem " + ec2_user + " 'chmod 700 check_webserver.py'"
        (status, output) = subprocess.getstatusoutput(cmd1)
        if status == 0:
            print('\nCheching Nginx status...')
            cmd = 'ssh -i BriansKey.pem ec2-user@' + instance[0].public_ip_address + ' python3 check_webserver.py'
            time.sleep(15)
            (status, output) = subprocess.getstatusoutput(cmd)
            print(output)
        else:
            print('Unable to execute check_webserver.py')
    else:
        print('check_webserver.py was not copied')


def create_s3_bucket():
    s3 = boto3.client('s3')

    try:
        bucket_number = randint(0, 1000)
        bucket_name = 'my-unique-bucket-' + str(bucket_number)  # Each bucket name must be wholly unique
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-west-1',  # Makes sure bucket created in same region as ec2 instance
            },
        )

        print('A new s3 bucket has been created:', bucket_name)
        data = 'hello_world.png'
        s3.upload_file(data, bucket_name, data)
        print('Hello World image uploaded to s3 bucket', bucket_name)

    except Exception as err:
        print(err)


def main():
    create_ec2_instance()
    create_s3_bucket()


if __name__ == '__main__':
    main()


