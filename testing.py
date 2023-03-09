import boto3
from moto import mock_dynamodb2
import JobTask

@mock_dynamodb2
def test_job_task_save_data():
    conn = boto3.resource('dynamodb', region_name='us-east-1')
    table = conn.create_table(TableName='test',
                                  KeySchema=[{'AttributeName': 'instance_id', 'KeyType': 'HASH'}],
                                  AttributeDefinitions=[{'AttributeName': 'ami_id', 'AttributeType': 'S'},
                                                        {'AttributeName': 'date_launched', 'AttributeType': 'S'}])

    worker = JobTask()
    worker.save_data(table, '0012abcd563', '1134abdc789', '04/02/2022, 14:50:10')

    response = table.get_item(Key={instance_id:'0012abcd563'})
    output = response['Item']

    print (response)


if __name ==  "__main__":
    test_job_task_save_data()