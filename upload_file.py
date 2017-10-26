import boto3


s3 = boto3.resource('s3')
object_name = 'Hello-World.jpg'


def upload_file():
    print('\nHere are all your current buckets;')
    for bucket in s3.buckets.all():
        print(bucket.name)

    chosen_bucket = input('\nPlease enter the name of the bucket you want to upload to: ')

    try:
        response = s3.Object(chosen_bucket, object_name).put(Body=open(object_name, 'rb'))
        print('The Hello-World.jpg image has been uploaded to ', chosen_bucket)

    except Exception as err:
        print(err)


def main():
    upload_file()


if __name__ == '__main__':
    main()