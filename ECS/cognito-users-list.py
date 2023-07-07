import boto3
from datetime import datetime, timedelta
from tabulate import tabulate

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
                user_info = {
                    'User ID': user['Username'],
                    'Preferred Username': '',
                    'Email': '',
                    'Creation Date': user['UserCreateDate']
                }
                attributes = user.get('Attributes', [])
                for attribute in attributes:
                    if attribute['Name'] == 'preferred_username':
                        user_info['Preferred Username'] = attribute['Value']
                    elif attribute['Name'] == 'email':
                        user_info['Email'] = attribute['Value']

                users.append(user_info)

        pagination_token = response.get('PaginationToken')

        if not pagination_token:
            break

    return users

# Usage
start_date = '2023-06-29'
end_date = '2023-07-04'

users = get_cognito_users(start_date, end_date)

# Prepare data for tabulate
table_data = []
for user in users:
    table_data.append([
        user['User ID'],
        user['Preferred Username'],
        user['Email'],
        user['Creation Date']
    ])

# Print tabulated user details
headers = ['User ID', 'Preferred Username', 'Email', 'Creation Date']
table = tabulate(table_data, headers, tablefmt='grid')
print(table)
