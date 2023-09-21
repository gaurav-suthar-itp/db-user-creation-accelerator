import boto3
import mysql.connector
import random,string,json
from botocore.exceptions import ClientError


# INPUTS
###########################################
users=['demo1','demo2']
db_identifier = "database-2-instance-1"
admin_username = 'admin'
admin_password = 'admin1234'
###########################################

aws_region = 'us-east-1'

##############################################################
################ CREATE A SECRET FOR EACH USER ###############
##############################################################

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

##############################################################
################ FETCH SECRETS FROM SECRET MANAGER ###########
##############################################################

def get_secret(user_secret):
    secret_name = f"rds/user/{user_secret}"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])
    credentials = {
        'username' : secret['username'],
        'password' : secret['password']
    }

    return credentials

credential_list =[]

for user in users:
    credential_list.append(get_secret(user))
    
rds = boto3.client('rds')

# Get the endpoint address of the RDS instance
response = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)
endpoint = response['DBInstances'][0]['Endpoint']['Address']

def execute_sql(sql_statement):
    try:
        connection = mysql.connector.connect(host=endpoint, user=admin_username, password=admin_password)
        for query in query_list:
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()
            print("SQL statement executed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        connection.close()


# Create the new user

query_list = []

for credentials in credential_list:
    username = credentials['username']
    password = credentials['password']

    query = f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'"

    query_list.append(query)

execute_sql(query_list)



