import boto3

class GetAndStoreDataJob:

    def get_instance_and_ami_ids(self, all_instances):
        instance_id, ami_id, date_launched = "", "", ""

        for r in all_instances['Reservations']:
            for instance in r['Instances']:
                instance_id = instance['InstanceId']
                ami_id = instance['ImageId']
                date_launched = instance['LaunchTime'].strftime("%m/%d/%Y, %H:%M:%S")

        return instance_id, ami_id, date_launched

    def save_data(self, table_name, instance_id, ami_id, date_launched):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table(table_name)

        table.put_item(
            Item={
                'instance_id': instance_id,
                'ami_id': ami_id,
                'date_launched': date_launched
            }
        )


if __name__ == "__main__":
    ec2 = boto3.client('ec2', region_name='us-east-1')

    all_instances = ec2.describe_instances()
    all_images = ec2.describe_images(Owners=['self'])

    worker = GetAndStoreDataJob()
    instance_id, ami_id, date_launched = worker.get_instance_and_ami_ids(all_instances)
    worker.save_data('instances-data', instance_id, ami_id, date_launched)
    print("Saved all data successfully!")

#print("===== Custom AMIs =====")
#for image in all_images['Images']:
    #print("ImageID :", image['ImageId'], "; Image name :", image['Name'],"; Creation date :", image['CreationDate'])
