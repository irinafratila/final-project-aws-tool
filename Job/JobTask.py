import boto3
import json
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
class GetAndStoreDataJob:

    def get_instance_and_ami_ids(self, all_instances):
        instance_data = [] # A list of dictionaries

        for r in all_instances['Reservations']:
            for instance in r['Instances']:
                if instance['State'] == {'Code': 16, 'Name': 'running'}:
                    instance_id = instance['InstanceId']
                    ami_id = instance['ImageId']
                    date_launched = instance['LaunchTime'].strftime("%m/%d/%Y, %H:%M:%S")
                    instance_data.append({
                        'instance_id': instance_id,
                        'ami_id': ami_id,
                        'date_launched': date_launched
                    })

        return instance_data

    def save_data(self, table_name, data):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table(table_name)

        for item in data:
            table.put_item(Item=item)


if __name__ == "__main__":
    ec2 = boto3.client('ec2', region_name='us-east-1')
    s3 = boto3.client('s3', region_name='us-east-1')
    s3_resource = boto3.resource('s3')

    bucket_name = 'running-instances-data-if1'
    key_name = 'running-ec2-instances.json'

    #all_instances = ec2.describe_instances()
    #
    #worker = GetAndStoreDataJob()
    #data = worker.get_instance_and_ami_ids(all_instances)
    #worker.save_data('instances-data',data)
    #print("Saved all data successfully!")

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

    #print(instance_data)

    # --- Check if running-ec2-instances.json already exists in the bucket ---
    for file in s3_resource.Bucket(bucket_name).objects.all():
        if file.key == key_name:
            # delete file
            s3.delete_object(Bucket=bucket_name,
                            Key=key_name)


    # --- Store data in S3 bucket ---
    try:
        ...
        #response = s3.put_object(Body=json.dumps(instance_data), Bucket=bucket_name, Key=key_name)
        #print(respond(None, response))

    except:
        print(respond(RuntimeError('Could not create S3 object of currently running instances')))




    print("===== Custom AMIs =====")
    ami_data_response = s3.get_object(
        Bucket='custom-amis-data-if1',
        Key='custom-amis-data.json',
    )
