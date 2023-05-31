import boto3

def get_first_access_keys_details():
    # Create a Boto3 client for CloudTrail
    cloudtrail_client = boto3.client('cloudtrail')

    # Create a Boto3 client for IAM
    iam_client = boto3.client('iam')

    # Retrieve a list of all IAM users
    response = iam_client.list_users()
    users = response['Users']

    # Initialize a dictionary to store user - access key details mappings
    user_access_keys = {}

    # Iterate over each IAM user
    for user in users:
        user_name = user['UserName']

        # Get a list of access keys for the user
        response = iam_client.list_access_keys(UserName=user_name)
        access_keys = response['AccessKeyMetadata']

        # Check if the user has any access keys
        if access_keys:
            first_access_key = access_keys[0]

            # Get the last utilized service and API call details for the first access key
            response = cloudtrail_client.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'AccessKeyId',
                        'AttributeValue': first_access_key['AccessKeyId']
                    }
                ],
                MaxResults=1,
                StartTime=first_access_key['CreateDate']
            )

            # Extract the last utilized service, API call details, and resource details from the CloudTrail event
            events = response.get('Events', [])
            if events:
                last_utilized_service = events[0]['EventName']
                event_source = events[0]['EventSource']
                event_name = events[0].get('EventName')
                resources = events[0]['Resources']
                event_origin = events[0].get('SourceIPAddress') or events[0].get('UserAgent')
                api_call_details = events[0].get('CloudTrailEvent', '')

                user_access_keys[user_name] = {
                    'AccessKeyId': first_access_key['AccessKeyId'],
                    'LastUtilizedService': last_utilized_service,
                    'EventSource': event_source,
                    'EventName': event_name,
                    'Resources': resources,
                    'Origin': event_origin,
                    'APICallDetails': api_call_details
                }

    return user_access_keys

# Example usage
access_keys_details = get_first_access_keys_details()
for user, details in access_keys_details.items():
    print(f"User: {user}")
    print(f"Access Key ID: {details['AccessKeyId']}")
    print(f"Last Utilized Service: {details['LastUtilizedService']}")
    print(f"Event Source: {details['EventSource']}")
    print(f"Event Name: {details['EventName']}")
    print(f"Origin: {details['Origin']}")
    print(f"API Call Details:\n{details['APICallDetails']}")
    print("Resources:")
    for resource in details['Resources']:
        print(f"\t- Resource Name: {resource['ResourceName']}")
        print(f"\t  Resource Type: {resource['ResourceType']}")
        print()
    print()
