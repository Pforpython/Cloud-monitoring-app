import boto3
import json
import os

# Replace with your own configurations
AWS_REGION = "us-east-1"
CLUSTER_NAME = "flask-app-cluster"
SERVICE_NAME = "flask-app-service"
TASK_FAMILY = "flask-app-task"
CONTAINER_NAME = "flask-container"
CONTAINER_PORT = 5000
IMAGE_URI = "<your_ecr_image_uri>"  # Replace with your ECR image URI

def register_task_definition():
    """
    Register a new task definition with the given Docker image URI.
    """
    ecs_client = boto3.client("ecs", region_name=AWS_REGION)

    print("Registering a new task definition...")
    response = ecs_client.register_task_definition(
        family=TASK_FAMILY,
        executionRoleArn="<execution_role_arn>",  # Replace with your ECS Task Execution Role ARN
        networkMode="awsvpc",
        containerDefinitions=[
            {
                "name": CONTAINER_NAME,
                "image": IMAGE_URI,
                "memory": 512,
                "cpu": 256,
                "essential": True,
                "portMappings": [
                    {
                        "containerPort": CONTAINER_PORT,
                        "hostPort": CONTAINER_PORT,
                        "protocol": "tcp"
                    }
                ]
            }
        ],
        requiresCompatibilities=["FARGATE"],
        cpu="256",
        memory="512",
    )
    print(f"Task definition registered: {response['taskDefinition']['taskDefinitionArn']}")
    return response["taskDefinition"]["taskDefinitionArn"]

def update_service(task_definition_arn):
    """
    Update the ECS service to use the new task definition.
    """
    ecs_client = boto3.client("ecs", region_name=AWS_REGION)

    print("Updating ECS service...")
    response = ecs_client.update_service(
        cluster=CLUSTER_NAME,
        service=SERVICE_NAME,
        taskDefinition=task_definition_arn,
        forceNewDeployment=True
    )
    print(f"ECS service updated: {response['service']['serviceName']}")

def main():
    """
    Main function to register task definition and update ECS service.
    """
    # Register the new task definition
    task_definition_arn = register_task_definition()

    # Update the ECS service
    update_service(task_definition_arn)

if __name__ == "__main__":
    main()
    
    
"""
How to Use the Script

	1.	Pre-Requisites:
	•	Make sure your AWS credentials are set up in the environment (via AWS CLI or environment variables like AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY).
	•	Install Boto3 if not already installed:
 
    pip install boto3
 
 	•	Replace placeholders like <your_ecr_image_uri> and <execution_role_arn> with actual values.
  
  	2.	Run the Script:
        Save this script as deploy_to_ecs.py and run it:
   
    python deploy_to_ecs.py
    
Code Explanation

	•	Task Definition:
	    - register_task_definition creates a new task definition specifying:
            •	Container name.
            •	Docker image (IMAGE_URI).
            •	CPU and memory requirements.
            •	Network mode (awsvpc) for Fargate compatibility.
            •	Port mapping to expose port 5000.
        
	•	Update ECS Service:
        •	update_service updates the ECS service to use the newly registered task definition.
        •	forceNewDeployment=True ensures that ECS deploys the new version immediately.
	
    •	Execution Role:
        - Ensure the ECS Task Execution Role has the necessary permissions to pull images from ECR and log data to CloudWatch.

"""