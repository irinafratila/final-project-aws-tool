import json
import boto3


def lambda_handler(event, context):
    s3 = boto3.client('s3', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    # Update data in S3 buckets before retrieving it and seding it thorugh the API
    update_buckets_response = lambda_client.invoke(FunctionName='auditingtool-updateInstancesAndImagesBuckets',
                                                   InvocationType='Event')

    if (update_buckets_response['StatusCode'] == 202):
        # Get instance and image data from their respective S3 buckets.
        instances_data_response = s3.get_object(
            Bucket='running-instances-data-if1',
            Key='running-ec2-instances.json')
        instances_json_to_send = instances_data_response["Body"].read().decode()

        ami_data_response = s3.get_object(
            Bucket='custom-amis-data-if1',
            Key='custom-amis-data.json')
        ami_json_to_send = ami_data_response["Body"].read().decode()

        # Building the body of the response to send back through
        # the API
        response = {
            'instances': instances_json_to_send,
            'amis': ami_json_to_send
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
