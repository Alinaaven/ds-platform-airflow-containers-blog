# Import necessary CDK modules
from aws_cdk import Stack, App
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from constructs import Construct

class MyEcsClusterStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create a new VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=3)
        
        # Create the ECS Cluster
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)
        
        # Create an ECS Task Role
        task_role = iam.Role(self, "ecsTaskRole", 
                             assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"), 
                             description="Role that the ECS task can assume")
        task_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy"))
        
        # Create an ECS Task Execution Role
        execution_role = iam.Role(self, "ecsExecutionRole", 
                                  assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"), 
                                  description="Task Execution Role that ECS can assume")
        execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryReadOnly"))
        execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess"))
        execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy"))

# Initialize the CDK App
app = App()
MyEcsClusterStack(app, "MyEcsClusterStack")
app.synth()
