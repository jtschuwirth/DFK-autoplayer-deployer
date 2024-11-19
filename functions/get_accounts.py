import os
import boto3
from dotenv import load_dotenv
load_dotenv()

def init_account_table():
    my_session = boto3.session.Session(
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
            region_name = "us-east-1",
        )

    return my_session.resource('dynamodb').Table("dfk-autoplayer-accounts")

def get_accounts(profession):
    accounts = []
    account_table = init_account_table()
    scan_response = account_table.scan(
            FilterExpression="enabled_quester = :enabled AND profession = :profession",
            ExpressionAttributeValues={
                ":enabled": True,
                ":profession": profession
            })
    for item in scan_response["Items"]:
        accounts.append(item["address_"])
    return accounts
