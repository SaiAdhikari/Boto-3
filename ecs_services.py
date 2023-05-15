import boto3
import botocore
import os
import time

# Initialize the ECS client
ecs = boto3.client('ecs')

# Define the cluster and service name
cluster = input("Please enter the cluster name: ")

desired_count = os.environ.get('DESIRED_COUNT')
if not desired_count:
    desired_count = int(input("Enter the desired count for the services: "))
else:
    desired_count = int(desired_count)
    
# Get the list of services in the cluster
response = ecs.list_services(cluster=cluster)
service_list = [arn.split("/")[-1] for arn in response['serviceArns']]

with open('services.txt', 'r') as f:
    service_names = f.read().splitlines()

# Update the service to stop new tasks from starting

for service_name in service_names:
    if service_name not in service_list:
        print(f"{service_name} is not present in the cluster, skipping...")
        continue
    response = ecs.update_service(cluster=cluster, service=service_name, desiredCount=desired_count)
    print(f"{service_name} desired count is set to {desired_count}")
    time.sleep(5)

"""
for service_name in service_names:
    try:
        response = ecs.update_service(cluster=cluster, service=service_name, desiredCount=desired_count)
        print(f"{service_name} desired count is set to {desired_count}")
    except (botocore.exceptions.ClusterNotFoundException, botocore.exceptions.ServiceNotFoundException) as e:
        print(f"Skipping {service_name} as it was not found in the cluster")
    except botocore.exceptions.ThrottlingException as e:
        print(f"API throttled. Waiting for 5 seconds and retrying the update service operation")
        time.sleep(5)
        response = ecs.update_service(cluster=cluster, service=service_name, desiredCount=desired_count)
        print(f"{service_name} desired count is set to {desired_count}")




for service_name in service_names:
    response = ecs.update_service(cluster=cluster, service=service_name, desiredCount=desired_count)
    print(f"{service_name} desired count is set to {desired_count}")
    time.sleep(5)


# Get the current running tasks of the service
for service_name in service_names:
    response = ecs.list_tasks(cluster=cluster, serviceName=service_name, desiredStatus='RUNNING')
    task_arns = response['taskArns']
    # Stop the tasks of the service
    if task_arns:
        response = ecs.stop_task(cluster=cluster, task=task_arns[0])
        print(f"Stopped task {task_arns[0]}")
    else:
        print("No running tasks to stop")
"""

