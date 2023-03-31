import boto3
import json
from datetime import datetime

dynamo = boto3.client('dynamodb', region_name='us-east-1')
ec2 = boto3.client('ec2', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
s3_resource = boto3.resource('s3')

# This function was automatically generated when I initiated
# the Lambda function using a template from them. The template
# is named "Create a microservice that interacts with a DDB table".
# This function is the only thing I kept from that template, I only changed the
# error code from '200' to '202'.
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '202',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    # --- Get instances that are running ---
    all_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
        ]
    )

    instance_data = []
    for r in all_instances['Reservations']:
        for instance in r['Instances']:
            instance_id = instance['InstanceId']
            ami_id = instance['ImageId']
            date_launched = instance['LaunchTime'].strftime("%d/%m/%Y, %H:%M:%S")
            instance_data.append({
                'instance_id': instance_id,
                'ami_id': ami_id,
                'date_launched': date_launched
            })

    # Check if running-ec2-instances.json already exists in the bucket,  delete it
    # if so. This is to refresh the resources and delete entries that have been terminated.
    for file in s3_resource.Bucket('running-instances-data-if1').objects.all():
        if file.key == 'running-ec2-instances.json':
            s3.delete_object(Bucket='running-instances-data-if1',
                             Key='running-ec2-instances.json')

    # --- Get data of AMIs that are custom-made by the user ----
    all_images = ec2.describe_images(Owners=['self'])
    images_data = []
    for image in all_images['Images']:
        image_id = image['ImageId']
        image_name = image['Name']
        creation_date = datetime.strptime(image["CreationDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
        creation_date = creation_date.strftime("%d/%m/%Y, %H:%M:%S")

        images_data.append({
            'image_id': image_id,
            'image_name': image_name,
            'creation_date': creation_date
        })

    # Check if custom-amis-data.json already exists in the bucket, delete it
    # if so. This is to refresh the resources and delete entries that have been terminated.
    for file in s3_resource.Bucket('custom-amis-data-if1').objects.all():
        if file.key == 'custom-amis-data.json':
            # delete file
            s3.delete_object(Bucket='custom-amis-data-if1',
                             Key='custom-amis-data.json')

    # --- Store data in S3 bucket ---
    try:
        instances_response = s3.put_object(Body=json.dumps(instance_data), Bucket='running-instances-data-if1',
                                           Key='running-ec2-instances.json')
        amis_response = s3.put_object(Body=json.dumps(images_data), Bucket='custom-amis-data-if1',
                                      Key='custom-amis-data.json')
        return respond(None, "Success")

    except:
        return respond(RuntimeError('Could not create S3 object of currently running instances or AMis'))
