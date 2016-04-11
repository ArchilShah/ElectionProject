from TwitterAPI import TwitterAPI
import json
import os

try:
    with open('credentials.json','r') as f:
        creds = json.loads(f.read())
        consumer_key = creds['consumer_key']
        consumer_secret = creds['consumer_secret']
        access_token_key = creds['access_token_key']
        access_token_secret = creds['access_token_secret']
        db_username = creds['db_username']
        db_password = creds['db_password']
except:
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token_key = os.environ['access_token_key']
    access_token_secret = os.environ['access_token_secret']
    db_username = os.environ['db_username']
    db_password = os.environ['db_password']

def get_api():
    return TwitterAPI(consumer_key,
                      consumer_secret,
                      access_token_key,
                      access_token_secret)

def get_db_credentials():
    return (db_username, db_password)
