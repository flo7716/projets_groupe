import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration DynamoDB
dynamodb = boto3.client(
    'dynamodb',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

table_name = 'articles'

try:
    response = dynamodb.describe_table(TableName=table_name)
    table_description = response['Table']

    # Print the key schema
    key_schema = table_description['KeySchema']
    print("Key Schema:")
    for key in key_schema:
        print(f"  AttributeName: {key['AttributeName']}, KeyType: {key['KeyType']}")

    # Print the attribute definitions
    attribute_definitions = table_description['AttributeDefinitions']
    print("\nAttribute Definitions:")
    for attr in attribute_definitions:
        print(f"  AttributeName: {attr['AttributeName']}, AttributeType: {attr['AttributeType']}")

except Exception as e:
    print(f"Error describing table: {e}")