from decouple import config
import requests, boto3, psycopg2, pandas as pd
from langchain_community.embeddings import BedrockEmbeddings
import base64
import numpy as np
import json
from confluent_kafka import Consumer
from datetime import datetime

def initialize_embeddings_model():
    boto3_bedrock = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=config("AWS_ACCESS_KEY"),
        aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-2",
    )
    embeddings_model = BedrockEmbeddings(
        model_id=config("BEDROCK_MODEL_ID_EMBEDDINGS"),
        client=boto3_bedrock,
    )
    return embeddings_model

embeddings_model = initialize_embeddings_model()

def get_embeddings(issue):
    print("inside get_embeddings function")
    try:
        print(issue, "issue data from kafka consumer\n")
        response = embeddings_model.embed_query("The filename is"+ str(issue['filename']) + "and the patch code is" + str(issue["patch"]))
        print(response, "get_embeddings response")
        if response:
            print("\nconversion done successfully\n") 
            return response 
        else:
            print("Embedding converstion unsuccessfull")  

    except Exception as e:
        print("Error in get_embeddings:", e)
