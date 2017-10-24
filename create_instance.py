#!usr/bin/env python3

import boto3
import time
import subprocess


def create_aws_server():
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
    time.sleep(60) # Halts program for 1 minute to allow the instance load before SSH is available
    instance[0].reload()
    cmd = "ssh -o StrictHostKeyChecking=no -i BriansKey.pem ec2-user@" + instance[0].public_ip_address + " 'pwd'"
    # Connects to instance via ssh
    #  -o provides options (suppresses the yes/no response from host key confirmation)

    print('Running command:', cmd)
    (status, output) = subprocess.getstatusoutput(cmd)
    if status == 0:
        print(output, '\nssh into ec2 instance successful')
    else:
        print('ssh failed')

    scp = 'scp -i BriansKey.pem check_webserver.py ec2-user@' + instance[0].public_ip_address +':.'
    (status, output) = subprocess.getstatusoutput(scp)
    if status == 0:
        print('Successfully copied check_webserver.py to ec2 instance\nChecking Nginx status')
        cmd = 'ssh -i BriansKey.pem ec2-user@' + instance[0].public_ip_address + ' python3 check_webserver.py'
        time.sleep(15)
        (status, output) = subprocess.getstatusoutput(cmd)
        print(output)
    else:
        print('check_webserver not copied')


def create_s3_bucket():
    s3 = boto3.resource('s3')
    try:
        bucket = s3.create_bucket(
            Bucket='aws_bucket',
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-west-1',  # Makes sure bucket created in same region as ec2 instance
            },
        )

        print('An amazon s3 bucket has been created with an id of: ', bucket[0].id)

    except Exception as err:
        print(err)


def main():
    create_aws_server()
    create_s3_bucket()


if __name__ == '__main__':
    main()


