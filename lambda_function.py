from functions.get_accounts import get_accounts
from functions.lambda_client import client
import json



def handler(event, context):
    c=0
    accounts_to_quest = []
    account_groups = []
    for account in get_accounts():
        if c==10: 
            account_groups.append(accounts_to_quest)
            accounts_to_quest = []
            c=0
        accounts_to_quest.append(account)
        c+=1
    if len(accounts_to_quest) > 0:
        account_groups.append(accounts_to_quest)
    for account_group in account_groups:
        print(f"running accounts: {account_group}" )
        client.invoke(
            FunctionName='dfk-autoplayer',
            InvocationType='Event',
            Payload= json.dumps({"users": account_group})
        )

