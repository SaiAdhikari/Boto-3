import boto3

def get_service_details(cluster_name, service_name):
    ecs_client = boto3.client('ecs')

    # Get the service details
    response = ecs_client.describe_services(
        cluster=cluster_name,
        services=[service_name]
    )

    if 'services' in response and len(response['services']) > 0:
        service = response['services'][0]

        # Get the desired information from the service details
        desired_count = service['desiredCount']
        running_count = service['runningCount']
        deployment_arn = service['deployments'][0]['taskDefinition']
        task_definition_arn = service['deployments'][0]['taskDefinition']
        task_definition_response = ecs_client.describe_task_definition(
            taskDefinition=task_definition_arn
        )
        container_definitions = task_definition_response['taskDefinition']['containerDefinitions']

        print(f"Service: {service_name}")
        print(f"Desired count: {desired_count}")
        print(f"Running count: {running_count}")
        print("Container details:")

        for container in container_definitions:
            container_name = container['name']
            container_image = container['image']
            container_image_digest = get_container_image_digest(cluster_name, container_name)

            print(f"Container name: {container_name}")
            print(f"Container image: {container_image}")
            print(f"Container image digest: {container_image_digest}")
            print("-------")

    else:
        print("Failed to retrieve service information.")

def get_container_image_digest(cluster_name, container_name):
    ecs_client = boto3.client('ecs')

    # List tasks for the given cluster
    response = ecs_client.list_tasks(
        cluster=cluster_name
    )

    if 'taskArns' in response and len(response['taskArns']) > 0:
        tasks = response['taskArns']

        for task in tasks:
            # Describe the task to get the container details
            response = ecs_client.describe_tasks(
                cluster=cluster_name,
                tasks=[task]
            )

            if 'tasks' in response and len(response['tasks']) > 0:
                task_details = response['tasks'][0]

                for container in task_details['containers']:
                    if container['name'] == container_name:
                        return container['imageDigest']

    return 'N/A'

# Usage
cluster_name = 'dev'
service_name = 'sellnetwork-1-0'

get_service_details(cluster_name, service_name)
