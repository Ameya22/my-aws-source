"""
Lambda Function to give random name from list of friends,
reads & writes config file into Amazon S3 bucket &
sends notification using Amazon SNS
"""
# __author__ = "Ameya Joshi"
# __credits__ = ["Ameya Joshi"]
# __maintainer__ = "Ameya Joshi"
# __email__ = "joshiamey22@gmail.com"

import json
import random
import boto3 # Python SDK for AWS

s3 = boto3.client('s3')
topic = boto3.client('sns')
bucket = 'my-lucky-draw-bucket'
key = 'config.json'


def give_random_name(names):
    """
    Select random name from names list
    :param names: List having names of friends
    """
    return random.choice(names)


def write_into_s3_file(writeobj):
    """
    Upload new data to a bucket
    :param writeobj: updated JSON data to upload
    """
    try:
        s3.put_object(
            Body=json.dumps(writeobj),
            Bucket=bucket,
            ACL='public-read-write',
            ContentType='application/json',
            Key=key)
    except Exception as err:
        print("Couldn't put object into S3 bucket: {}".format(err))


def read_object_from_s3():
    """
    Gets an object from bucket & reads content from the object
    """
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body']
        return json.loads(content.read())
    except Exception as err:
        print("Couldn't get object from S3 bucket: {}".format(err))


def publish_msg(message):
    """
    Publish message to the topic created using Amazon SNS
    :param message: Message to publish
    """
    try:
        resp = topic.publish(
            TargetArn="arn:aws:sns:us-east-1:647569116701:BC-Lucky-Draw",
            Message=json.dumps({'default': message}),
            MessageStructure='json')
        print("Published message successfully")
        return resp
    except Exception as error:
        print("Couldn't publish message: {}".format(error))
        return error


def lambda_handler(event, context):
    # TODO implement
    bc_friends = ['Ameya', 'Ashish', 'Ashutosh', 'Mandar', 'Nakul', 'Ojas', 'Rohit', 'Tanmay']

    def check_availability(nam, names_lst):
        print("Name:: {}".format(nam))
        if nam in names_lst:
            print("name available in the list")
            noun = give_random_name(bc_friends)
            name_list = jsonobj['names']
            n = check_availability(noun, name_list)
            return str(n)
        else:
            return str(nam)

    jsonobj = read_object_from_s3()
    print(jsonobj)
    c = jsonobj['count']
    if c == 8:
        jsonobj['count'] = 0
        print("8 months --> 1 round of BC completed")
        jsonobj['names'] = []
        write_into_s3_file(jsonobj)
        alert = "8 months --> 1 round of BC completed"
        resp = publish_msg(alert)
    else:
        name = give_random_name(bc_friends)
        names_list = jsonobj['names']
        star = check_availability(name, names_list)
        for k, v in jsonobj.items():
            if k == 'names':
                jsonobj['names'].append(star)
        jsonobj['count'] = c + 1
        write_into_s3_file(jsonobj)
        message = "Hi, Send BC amount to {} for this month".format(star)
        resp = publish_msg(message)

    return {
        'statusCode': 200,
        'body': json.dumps(resp)
    }
