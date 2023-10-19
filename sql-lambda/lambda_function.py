import boto3
import pymysql  
import json

def execute_sql_script(sql_script, db_connection):
    cursor = db_connection.cursor()
    sql_commands = sql_script.split(';')

    for command in sql_commands:
        if command.strip():
            print(f'Executing SQL : {command}')
            cursor.execute(command)
    
    db_connection.commit()

def get_secret(secret_name):
    region_name = "us-east-1" 
    
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = response['SecretString']
        secret_dict = json.loads(secret)
        print(f'Secret - {secret_name} fetched successfully')
        return secret_dict
    except Exception as e:
        raise Exception(f"Failed to retrieve secret {secret_name}: {str(e)}")
        
def get_ssm_parameter(parameter_name):
    ssm = boto3.client('ssm')
    
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        print(f'Parameter - {parameter_name} fetched successfully')
        return response['Parameter']['Value']
    except Exception as e:
        raise Exception(f"Failed to retrieve SSM parameter {parameter_name}: {str(e)}")

def lambda_handler(event, context):

    ssm_db_endpoint = event.get('ssm_db_endpoint')
    ssm_database_name = event.get('ssm_database_name')
    secret_name = event.get('secret_name')
    region_name = event.get('region_name')
    script_filename = 'input.sql'
    
    try:
        
        with open(script_filename, 'r') as file:
            script_content = file.read()
            
        db_host = get_ssm_parameter(ssm_db_endpoint)
        db_name = get_ssm_parameter(ssm_database_name)

        
        secret_data = get_secret(secret_name)
        
        db_connection = pymysql.connect(
            host=db_host,  # Replace with your custom port
            user=secret_data['username'],
            password=secret_data['password'],
            database=db_name
        )

        execute_sql_script(script_content, db_connection)

        return {
            'statusCode': 200,
            'body': 'SQL script executed successfully.'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }