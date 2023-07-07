import boto3
from datetime import datetime, timedelta

def get_cognito_users(start_date, end_date):
    client = boto3.client('cognito-idp')
    user_pool_id = 'us-east-1_WPhcg35bJ'
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    
    users = []
    pagination_token = None
    
    while True:
        if pagination_token:
            response = client.list_users(
                UserPoolId=user_pool_id,
                PaginationToken=pagination_token
            )
        else:
            response = client.list_users(UserPoolId=user_pool_id)
        
        for user in response['Users']:
            created_date = user['UserCreateDate']
            created_date = datetime.strptime(created_date.strftime('%Y-%m-%d'), '%Y-%m-%d')
            
            if start_date <= created_date < end_date:
                users.append(user)
        
        pagination_token = response.get('PaginationToken')
        
        if not pagination_token:
            break
    
    return users

# Usage
start_date = '2023-06-29'
end_date = '2023-07-04'

users = get_cognito_users(start_date, end_date)

# Print the list of users
for user in users:
    print(user['Username'])
