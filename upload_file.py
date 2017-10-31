import boto3
import subprocess


s3 = boto3.resource('s3')
s3Client = boto3.client('s3')
ec2 = boto3.resource('ec2')
object_name = 'Hello-World.jpg'


# Method to stop users from crashing program if trying to upload file with no buckets
def check_buckets():
    bucket_list = []
    for bucket in s3.buckets.all():
        bucket_list.append(bucket)

    if len(bucket_list) > 0:
        upload_file_bucket()
    else:
        print('It looks like you dont have any buckets.\nYou should try making some first!')


# Method which allows user to choose a bucket to upload the Hello-Word file to
# and launch it on an instance
def upload_file_bucket():
    # Prints all current buckets and places them in an array for easy user selection
    print('\nHere are all your current buckets;')
    index_number = 1
    bucket_list = []
    for bucket in s3.buckets.all():
        print(index_number, ')', bucket.name)
        index_number += 1
        bucket_list.append(bucket)

    # Prompts user for input and selects the bucket from the array based on this
    index = input('\nPlease enter the index of the bucket you want to upload to: ')
    chosen_bucket = bucket_list[int(index)-1]

    try:
        # Method which takes the local Hello-World.jpg and pushes it to the created bucket
        s3.Object(chosen_bucket.name, object_name).put(Body=open(object_name, 'rb'))
        print('The Hello-World.jpg image has been uploaded to ', chosen_bucket)

        # Grant the object read permissions
        hello_world = s3.Bucket(chosen_bucket.name).Object(object_name)
        hello_world.Acl().put(ACL='public-read')
        print('Giving the Hello-World.jpg read permissions')

        print('\nWould you like to add this file to one of your ec2 instances? [Y/N]')
        answer = input('->')

        if answer.upper() == 'Y':

            instance_list = []
            for instance in ec2.instances.all():
                if instance.state['Name'] == 'running':
                    instance_list.append(instance)

            if len(instance_list) > 0:
                upload_file_instance(chosen_bucket)
            else:
                print('It looks like you don\'t have any running instances.'
                      '\nYou should try making some first!')

    except Exception as err:
        print(err)


def upload_file_instance(chosen_bucket):
    try:
        url = "https://s3-eu-west-1.amazonaws.com/" + chosen_bucket.name + "/" + object_name
        # Prints all instances and places them in an array for easy user selection
        index_number = 1
        instance_list = []
        print('\nHere are all your currently running instances;')
        for instance in ec2.instances.all():
            if instance.state['Name'] == 'running':
                print(index_number, ')', instance)
                index_number += 1
                instance_list.append(instance)

        # Prompts user for input and selects the instance from the array based on this
        index = input('Please enter the index of the instance you want to upload to: ')
        chosen_instance = instance_list[int(index) - 1]

        # Command to overwrite the current nginx home page of the chosen instance
        cmd = " 'echo \"<html><p>Here is the uploaded s3 image</p>" \
              "<img src=" + url + " alt=\'Hello-World\'/></html>\" " \
              "| sudo tee -a /usr/share/nginx/html/index.html'"
        print('Running command: ' + cmd)
        # SSH into the chosen instance and execute the command to view the bucket image
        (status, output) = subprocess.getstatusoutput('ssh -o StrictHostKeyChecking=no -i BriansKey.pem ec2-user@'
                                                  + chosen_instance.public_ip_address
                                                  + cmd)
        if status == 0:
            print('\nThe file has successfully been uploaded to', 'https://'
                  + chosen_instance.public_ip_address)
        else:
            print(output, '\nUnfortunately the image couldn\'t be uploaded')

    except Exception as err:
        print(err)


def main():
    check_buckets()


if __name__ == '__main__':
    main()
