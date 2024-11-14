import boto3

client = boto3.client('ecr')

reposity_name = "cloud_monitoring_app"

response = client.create_repository(
    repositoryName=reposity_name
)

repository_URI = response['repository']['repositoryUri']
print(repository_URI)




