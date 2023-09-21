import boto3
import json

# Specify the name of the secret you want to retrieve
secret_name = "rds/user/admin"

# Create an AWS Secrets Manager client
secrets_client = boto3.client('secretsmanager')

try:
    # Get the secret value
    response = secrets_client.get_secret_value(SecretId=secret_name)

    # If the secret has a 'SecretString' field, it's a JSON string
    if 'SecretString' in response:
        secret = json.loads(response['SecretString'])
        username=secret['username']
        password = secret['password']
        print(username + " " + password)
    else:
        # If the secret doesn't have a 'SecretString' field, it's a binary secret
        # You can access it using response['SecretBinary']
        print("Binary secret:", response['SecretBinary'])

except Exception as e:
    print(f"Error: {str(e)}")
