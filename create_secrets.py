import boto3
import random
import string,json

# USERS TO BE CREATED
###########################################
users=['demo','demo1']
###########################################

aws_region = 'us-east-1'

session = boto3.session.Session(region_name=aws_region)
secrets_manager_client = session.client('secretsmanager')

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

secrets=[]

for user in users:
    password = generate_random_string(12)
    secret_data = {
        'username': user,
        'password': password
    }
    secrets.append(secret_data)

print(secrets)

for secret_data in secrets:
    username = secret_data['username']
    secret_name = f'rds/user/{username}'

    response = secrets_manager_client.create_secret(
        Name=secret_name,
        SecretString=json.dumps(secret_data)
    )

    if 'ARN' in response:
        print(f'Secret "{secret_name}" created successfully.')
    else:
        print('Failed to create the secret.')
