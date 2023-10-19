import boto3
import os
import pymysql
import random,string,json
from botocore.exceptions import ClientError

##############################################################
########################## INPUTS ############################
##############################################################
users=(os.environ['users']).split(",")
db_endpoint = os.environ['db_endpoint']
admin_secret_name = os.environ['admin_secret_name']
aws_region = os.environ['aws_region']
##############################################################
################ FETCH SECRETS FROM SECRET MANAGER ###########
##############################################################

def get_secret(user_secret):
    print(f'Fetching Secret of {user_secret}...')
    if user_secret is admin_secret_name:
        secret_name = admin_secret_name
    else:
        secret_name = f"rds/user/{user_secret}"

    region_name = aws_region
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
    except:
        return False

    secret = json.loads(get_secret_value_response['SecretString'])
    credentials = {
        'username' : secret['username'],
        'password' : secret['password']
    }

    return credentials

##############################################################
################ CREATE A SECRET FOR EACH USER ###############
##############################################################
for user in users:
        print(f'Creating secret for {user} ...')
        session = boto3.session.Session(region_name=aws_region)
        secrets_manager_client = session.client('secretsmanager')

        def generate_random_string(length):
            characters = string.ascii_letters + string.digits
            return ''.join(random.choice(characters) for i in range(length))

        secrets=[]

        
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
    



admin_secret = get_secret(admin_secret_name)

admin_username = admin_secret['username']
admin_password = admin_secret['password']

credential_list =[]

for user in users:
    credential_list.append(get_secret(user))

##############################################################
############ DB-CONNECTION AND QUERY-EXECUTION ###############
##############################################################

def execute_sql(sql_statement):
    try:
        connection = pymysql.connect(host=db_endpoint, user=admin_username, password=admin_password)
        for query in query_list:
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()
            print("SQL statement executed successfully.")
    except Exception as e:
        print(f"SQL Error: {str(e)}")
    finally:
        connection.close()

query_list = []

for credentials in credential_list:
    username = credentials['username']
    password = credentials['password']
    query = f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'"
    query_list.append(query)

execute_sql(query_list)