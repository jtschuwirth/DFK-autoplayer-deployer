from functions.get_accounts import get_accounts
from functions.lambda_client import client
from functions.data import init_settings_table, init_account_table
import json



def handler(event, context):
    setup = event["setup"] if "setup" in event else "traditional"
    settings_table = init_settings_table()
    if setup == "traditional":
        settings = settings_table.get_item(Key={"key_": "autoplayer_settings"})["Item"]
    elif setup == "short":
        settings = settings_table.get_item(Key={"key_": "autoplayer_short_settings"})["Item"]

    current_invocation = int(settings["current_invocation"])
    target_invocation = int(settings["target_invocations"])
    
    if setup == "traditional":
        settings_table.update_item(
            Key={"key_": "autoplayer_settings"},
            UpdateExpression="SET current_invocation = :current_invocation",
            ExpressionAttributeValues={
                ":current_invocation": current_invocation+1
            }
        )
        if target_invocation-1 <= current_invocation: 
            settings_table.update_item(
                Key={"key_": "autoplayer_settings"},
                UpdateExpression="SET current_invocation = :current_invocation",
                ExpressionAttributeValues={
                    ":current_invocation": 0
                }
            )
    elif setup == "short":
        settings_table.update_item(
            Key={"key_": "autoplayer_short_settings"},
            UpdateExpression="SET current_invocation = :current_invocation",
            ExpressionAttributeValues={
                ":current_invocation": current_invocation+1
            }
        )
        if target_invocation-1 <= current_invocation: 
            settings_table.update_item(
                Key={"key_": "autoplayer_short_settings"},
                UpdateExpression="SET current_invocation = :current_invocation",
                ExpressionAttributeValues={
                    ":current_invocation": 0
                }
            )
    c=0
    accounts = []
    accounts_to_quest = []
    account_groups = []
    accounts_table = init_account_table()
    if setup == "traditional":
        accounts += get_accounts("mining")
        accounts += get_accounts("gardening")
    elif setup == "short":
        accounts += get_accounts("fishing")
        accounts += get_accounts("foraging")
    for account in accounts:
        if int(account, 16)%target_invocation != current_invocation: continue
        accounts_table.update_item(
            Key={"address_": account},
            UpdateExpression="SET questing = :questing",
            ExpressionAttributeValues={
                ":questing": False
            }
        )
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
            Payload= json.dumps({"users": account_group, "chain": "dfk"})
        )

