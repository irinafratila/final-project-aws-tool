import boto3
from JobTask import GetAndStoreDataJob
from moto import *

@mock_dynamodb
def test_job_task_save_data():
    conn = boto3.client('dynamodb', region_name='us-east-1')
    table = conn.create_table(TableName='test',
                              KeySchema=[ {'AttributeName': 'instance_id', 'KeyType': 'HASH'}],
                              AttributeDefinitions=[{'AttributeName': 'instance_id', 'AttributeType': 'S'}],
                              ProvisionedThroughput={
                                  'ReadCapacityUnits': 123,
                                  'WriteCapacityUnits': 123
                              }
    )

    worker = GetAndStoreDataJob()
    worker.save_data('test', '0012abcd563', '1134abdc789', '04/02/2022, 14:50:10')

    response = table.get_item(Key={instance_id:'0012abcd563'})
    output = response['Item']

    print(response)


if __name__ == "__main__":
    test_job_task_save_data()