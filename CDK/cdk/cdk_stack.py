import logging,string,random

from aws_cdk import (
    Stack,
    aws_secretsmanager as secretsmanager,
    CfnOutput,
    Fn
)
from constructs import Construct

import sys

class CdkStack(Stack):
    def __init__(self, scope: Construct, id: str,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        print("print")

        # secrets = []
        # def generate_random_string(length):
        #     characters = string.ascii_letters + string.digits
        #     return ''.join(random.choice(characters) for i in range(length))

        # users = ['demo1','demo2']

        # for user in users:
        #     password = generate_random_string(12)
        #     secret_data = {
        #         'username': user,
        #         'password': password
        #     }
        #     secrets.append(secret_data)


        # if secrets is None:
        #     raise LookupError("Secrets is missing in the context ")

        # for secret in secrets:
        #     logging.info("Creating Secrets in Secrets Manager")
        #     scrt = secretsmanager.CfnSecret(
        #         self,
        #         "Secret_" + secret['username'],
        #         name=secret['username'],
        #         secret_string=secret['password'],
        #         tags=[{
        #             "key": "Name",
        #             "value": secret['username']
        #         }]
        #     )
        #     CfnOutput(self, secret['username']+"id", export_name=secret['username'].replace("_","-"), value=scrt.ref)

        admin_secret = secretsmanager.Secret.from_secret_name_v2(self, "AdminSecret", "rds/user/admin")
        username = admin_secret.secret_name
        