import json
import boto3

# When a GET request comes through the API, it will be directed to this function.
# This function will get the instances and images data stored in their respective
# S3 buckets, format it, and send it back to be displayed on the website.
def lambda_handler(event, context):
    s3 = boto3.client('s3', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    # Invoking the respective Lambda function asynchronously, which will update the S3 buckets
    # before getting the data and sending it back here.
    # Adapted from AWS Boto3/Lambda/Client documentation
    # Accessible at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
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
