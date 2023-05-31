import boto3

def get_access_key_api_logs(access_key_id):
    # Create a Boto3 client for CloudTrail
    cloudtrail_client = boto3.client('cloudtrail')

    # Search for the CloudTrail events associated with the access key
    response = cloudtrail_client.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'AccessKeyId',
                'AttributeValue': access_key_id
            }
        ],
        MaxResults=50,  # Maximum number of events to retrieve (adjust as needed)
        StartTime='2023-05-01',  # Specify the start time for the search (adjust as needed)
        EndTime='2023-05-31'  # Specify the end time for the search (adjust as needed)
    )

    # Extract the API call details from the CloudTrail events
    events = response.get('Events', [])

    api_logs = []

    # Iterate over each CloudTrail event
    for event in events:
        api_event = {}

        # Extract relevant fields from the event
        event_name = event['EventName']
        event_time = event['EventTime']
        event_source = event['EventSource']
        event_user = event['Username']
        event_ip = event.get('SourceIPAddress')
        event_user_agent = event.get('UserAgent')

        # Store the API call details
        api_event['EventName'] = event_name
        api_event['EventTime'] = event_time
        api_event['EventSource'] = event_source
        api_event['Username'] = event_user
        api_event['SourceIPAddress'] = event_ip
        api_event['UserAgent'] = event_user_agent

        # Append the API event to the logs list
        api_logs.append(api_event)

    return api_logs


def get_access_keys_api_logs():
    # Create a Boto3 client for IAM
    iam_client = boto3.client('iam')

    # Retrieve a list of all IAM users
    response = iam_client.list_users()
    users = response['Users']

    # Initialize a dictionary to store user - access key logs mappings
    user_access_keys_logs = {}

    # Iterate over each IAM user
    for user in users:
        user_name = user['UserName']

        # Get a list of access keys for the user
        response = iam_client.list_access_keys(UserName=user_name)
        access_keys = response['AccessKeyMetadata']

        # Check if the user has any access keys
        if access_keys:
            first_access_key = access_keys[0]
            access_key_id = first_access_key['AccessKeyId']

            # Get the API logs for the access key
            api_logs = get_access_key_api_logs(access_key_id)

            # Store the logs for the access key
            user_access_keys_logs[user_name] = {
                'AccessKeyId': access_key_id,
                'APILogs': api_logs
            }

    return user_access_keys_logs


# Example usage
access_keys_logs = get_access_keys_api_logs()
for user, logs in access_keys_logs.items():
    print(f"User: {user}")
    print(f"Access Key ID: {logs['AccessKeyId']}")
    print("API Logs:")
    for api_log in logs['APILogs']:
        print(f"Event Name: {api_log['EventName']}")
        print(f"Event Time: {api_log['EventTime']}")
        print(f"Event Source: {api_log['EventSource']}")
        print