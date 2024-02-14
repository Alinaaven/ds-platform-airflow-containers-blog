# ds-platform-airflow-containers-blog

This project demonstrates an end-to-end workflow for deploying and running containerized tasks on AWS ECS via Apache Airflow, including infrastructure provisioning with AWS Cloud Development Kit (CDK), task definition creation via AWS CLI, and continuous integration and deployment (CI/CD) with Azure Pipelines.

Project Structure
dags/ - Contains Airflow DAG files for ECS tasks execution.
cdk/ - AWS CDK scripts for provisioning ECS clusters and related resources.
pipelines/ - Azure Pipeline YAML configuration for CI/CD processes.

Prerequisites
AWS Account and CLI configured with necessary permissions.
Azure DevOps account and an Azure Container Registry (ACR).
Apache Airflow environment setup.
AWS Cloud Development Kit (CDK) installed.
Docker installed locally or in CI/CD environment.
Setup and Deployment
1. Infrastructure Provisioning with AWS CDK
Navigate to the cdk/ directory and deploy the ECS cluster and related resources:

cd cdk/
cdk deploy

2. Task Definition Creation with AWS CLI
Create a new ECS task definition with the necessary configurations:
Run the command in the aws_register_task_definition file.


4. Airflow DAG Configuration
Place your DAG files in the Airflow dags/ directory. Ensure your DAG utilizes the EcsRunTaskOperator with parameters specified in external parameter files or environment variables.

5. Building and Pushing Docker Images with Azure Pipeline
The Azure Pipeline defined in pipelines/azure-pipeline.yml automates the process of building the Docker image, running tests, and pushing the image to AWS Elastic Container Registry (ECR).

Configure the pipeline in your Azure DevOps project and link it to your repository.

Azure Pipeline Configuration
The pipeline uses the following stages:

Build: Builds the Docker image based on the Dockerfile.
Push: Pushes the built image to AWS ECR.
Make sure to replace placeholders in the azure-pipeline.yml with your actual AWS ECR repository URI and credentials.

Running the Airflow DAG
Once everything is set up, trigger the DAG run from the Airflow UI or CLI. The DAG should execute the ECS task based on the task definition and parameters specified.

Monitoring and Logs
Monitor the execution of ECS tasks through the AWS Management Console. Logs can be accessed via Amazon CloudWatch if configured in the task definition.

Cleanup
Remember to clean up resources to avoid unnecessary charges:

cdk destroy

And deregister the ECS task definition if no longer needed:

aws ecs deregister-task-definition --task-definition <taskDefinitionArn>
