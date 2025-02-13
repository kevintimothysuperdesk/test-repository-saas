import json
import os
import boto3
# from utils.error_logger import insert_error_log
from dotenv import load_dotenv
load_dotenv()

# PS_FET_SEC_4.2 - PS_FET_SEC_4.19 - fetch the creditienital from secret manager.based on the  secret_type/

def fetch_secret(secret_type=None):
    try:
        # SEQ_FET_SEC_4.4: Create AWS SecretsManager boto3 client
        client = boto3.client(
            service_name='secretsmanager',
            region_name=os.getenv('AWS_REGION')  # Ensure AWS_REGION is set in your environment
        )

        # SEQ_FET_SEC_4.6: Call get_secret_value to retrieve secret
        response = client.get_secret_value(
            SecretId=os.getenv('SECRET_ID')  # Ensure SECRET_ID is set in your environment
        )

        # SEQ_FET_SEC_4.8: Check if SecretString is in response
        if 'SecretString' not in response:
            raise Exception('Secret string is not present in the response')
        
        # SEQ_FET_SEC_4.9: Parse the secret string from the response
        secrets = json.loads(response['SecretString'])
       
        # SEQ_FET_SEC_4.10 to SEQ_FET_SEC_4.14: Return appropriate secrets based on secret_type
        if secret_type == 'db_secrets':
            return {k: secrets[k] for k in ('DB_HOST', 'DB_PORT', 'DB_DATABASE', 'DB_PASSWORD', 'DB_USER')}
        elif secret_type == 's3_secrets':
            return {'S3_BUCKET_NAME': secrets['S3_BUCKET_NAME']}
        elif secret_type == 'gateway_secrets':
            return {'GATEWAY_URL': secrets['GATEWAY_URL']}
        elif secret_type == 'aws_secrets':
            return {k: secrets[k] for k in ('ACCESS_KEY', 'SECRET_KEY')}
        elif secret_type == 'cognito_secrets':
            return {k: secrets[k] for k in ('COGNITO_REGION', 'COGNITO_POOL_ID')}
        # Return all secrets if secret_type is 'all_secret' or None
        return secrets

    except Exception as e:
        print("Error form fetch_secret :",e)
        raise str(e)