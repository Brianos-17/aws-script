#!usr/bin/env python3

import boto3
import time
import subprocess


def create_ec2_instance():
    ec2 = boto3.resource('ec2')

    try:
        # Creates the ec2 instance with its variables
        instance = ec2.create_instances(
            ImageId='ami-acd005d5',
            MinCount=1,
            MaxCount=1,
            KeyName='BriansKey',
            SecurityGroupIds=['sg-ed51b996'],
            # User Data installs python 3.5 and Nginx
            UserData='''#!/bin/bash
                    yum -y update
                    yum -y install python35        
                    yum -y install nginx 
                    service nginx start
                    chkconfig nginx on''',
            InstanceType='t2.micro')

        print('An instance has been created with an ID of: ' + instance[0].id)
        time.sleep(5)
        instance[0].reload()
        print('The new instance has a public IP address of: '+  instance[0].public_ip_address)

        instance[0].create_tags(
            Resources=[instance[0].id],
            Tags=[
                {
                    'Key': 'Name',  # Calling the Key "Name" ensures it appears on the default view
                    'Value': 'Dev_Ops_Assignment'
                },
            ]
        )

        print('The instance', instance[0].id, 'has been given a new tag')

        ec2_user = 'ec2-user@' + instance[0].public_ip_address # Ec2 users address

        # Connects to instance via ssh
        #  -o provides options (suppresses the yes/no response from host key confirmation)
        cmd = "ssh -o StrictHostKeyChecking=no -i BriansKey.pem " + ec2_user + " 'pwd'"
        print('\nRunning command:', cmd)

        time.sleep(60)  # Halts program for 1 minute to allow the instance load before SSH is available
        instance[0].reload()
        (status, output) = subprocess.getstatusoutput(cmd)  # Runs the cmd command
        if status == 0:
            print('\nssh into ec2 instance successful', output)
        else:
            print('ssh failed\n')

        # Copies the check_websever file into the ec2 machine to be run locally
        scp = 'scp -i BriansKey.pem check_webserver.py ' + ec2_user + ':.'
        (status, output) = subprocess.getstatusoutput(scp)

        if status == 0:
            print('\nSuccessfully copied check_webserver.py to ec2 instance'
                  '\nGranting executable privilages for check_webserver.py')
            cmd1 = 'ssh -i BriansKey.pem ' + ec2_user + ' "chmod 700 check_webserver.py"'
            (status, output) = subprocess.getstatusoutput(cmd1)  # Runs cmd1 command

            if status == 0:
                print('\nChecking Nginx status...')
                cmd = 'ssh -i BriansKey.pem ' + ec2_user + ' "python3 check_webserver.py"'
                time.sleep(15)
                (status, output) = subprocess.getstatusoutput(cmd)
                print(output)

            else:
                print('Unable to execute check_webserver.py')

        else:
            print('check_webserver.py was not copied')

    # Exits method gracefully if error is encountered
    except Exception as err:
        print(err)


def main():
    create_ec2_instance()


if __name__ == '__main__':
    main()
