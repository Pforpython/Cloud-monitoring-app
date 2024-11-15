# Provisioning ECS and Fargate Resources
# Below is a script to provision the ECS cluster and service if they don’t already exist. You can integrate this with the original script.

import boto3

AWS_REGION = "us-east-1"
CLUSTER_NAME = "flask-app-cluster"
SERVICE_NAME = "flask-app-service"
TASK_FAMILY = "flask-app-task"
SUBNETS = ["<subnet-1>", "<subnet-2>"]  # Replace with your VPC subnet IDs
SECURITY_GROUP = "<security-group-id>"  # Replace with your security group ID
ROLE_ARN = "<execution-role-arn>"  # Replace with your ECS task execution role ARN

def create_ecs_cluster():
    """
    Create an ECS cluster if it doesn't already exist.
    """
    ecs_client = boto3.client("ecs", region_name=AWS_REGION)

    print(f"Creating ECS cluster: {CLUSTER_NAME}...")
    response = ecs_client.create_cluster(clusterName=CLUSTER_NAME)
    print(f"ECS cluster created: {response['cluster']['clusterArn']}")

def create_ecs_service(task_definition_arn):
    """
    Create an ECS service using Fargate.
    """
    ecs_client = boto3.client("ecs", region_name=AWS_REGION)

    print(f"Creating ECS service: {SERVICE_NAME}...")
    response = ecs_client.create_service(
        cluster=CLUSTER_NAME,
        serviceName=SERVICE_NAME,
        taskDefinition=task_definition_arn,
        desiredCount=1,
        launchType="FARGATE",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": SUBNETS,
                "securityGroups": [SECURITY_GROUP],
                "assignPublicIp": "ENABLED",
            }
        },
    )
    print(f"ECS service created: {response['service']['serviceArn']}")

def main():
    """
    Main function to provision ECS cluster and service.
    """
    # Create the ECS cluster
    create_ecs_cluster()

    # Assume the task definition is already registered
    task_definition_arn = "<task-definition-arn>"  # Replace with the ARN of your task definition

    # Create the ECS service
    create_ecs_service(task_definition_arn)

if __name__ == "__main__":
    main()
    
    
"""
Steps in the Script

	1.	create_ecs_cluster:
	•	Provisions an ECS cluster if it doesn’t exist.
	•	This is required to manage ECS tasks and services.
	2.	create_ecs_service:
	•	Provisions an ECS service to manage the deployment of tasks using Fargate.
	•	Configures networking with subnets, security groups, and public IP assignment.

Integration with the Original Script

	1.	Use the cluster and service creation functions above if they don’t already exist.
	2.	After registering the task definition, call the service creation function to deploy it.

Pre-Requisites

	1.	Subnets and Security Groups:
	•	Ensure the subnets are in the same VPC and have internet access (via NAT or IGW).
	•	The security group must allow inbound traffic on port 5000.
	2.	IAM Roles:
	•	Ensure the executionRoleArn has permissions to:
	•	Pull images from ECR.
	•	Log to CloudWatch.
"""