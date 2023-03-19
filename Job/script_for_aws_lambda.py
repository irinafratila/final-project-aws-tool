import boto3
import json

dynamo = boto3.client('dynamodb', region_name='us-east-1')
ec2 = boto3.client('ec2', region_name='us-east-1')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }



def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    # operation = event['httpMethod']


    # --- Get instance IDs ---
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

    instance_data = []  # A list of dictionaries

    for r in all_instances['Reservations']:
        for instance in r['Instances']:
            instance_id = instance['InstanceId']
            ami_id = instance['ImageId']
            date_launched = instance['LaunchTime'].strftime("%m/%d/%Y, %H:%M:%S")
            instance_data.append({
                'instance_id': instance_id,
                'ami_id': ami_id,
                'date_launched': date_launched
            })

            # --- Put item in DynamoDB ---
            put_query = dynamo.put_item(TableName='instances-data',
                                        Item={
                                            'instance_id': {
                                                'S': instance_id},
                                            'ami_id': {
                                                'S': ami_id},
                                            'date_launched': {
                                                'S': date_launched}

                                        })

    print(instance_data)

    # save_data('instances-data',instance_data)
    # return respond(None, instance_data)

    # if operation in operations:
    # payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
    # return respond(None, operations[operation](dynamo, payload))
    # else:
    # return respond(ValueError('Unsupported method "{}"'.format(operation)))
