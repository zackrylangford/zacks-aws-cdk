#!/usr/bin/env python3
from aws_cdk import (
    App,
    Stack,
    aws_dynamodb as dynamodb,
    aws_ec2 as ec2,
)
from constructs import Construct

# Import your custom library
from my_cdk_lib.compute import LambdaFunction, StandardEC2Instance
from my_cdk_lib.storage import SecureS3Bucket
from my_cdk_lib.database import EnhancedDynamoTable
from my_cdk_lib.networking import StandardVpc
from my_cdk_lib.security import CommonSecurityGroups
from my_cdk_lib.patterns import ServerlessApi, StaticWebsite


class ExampleStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a standard VPC
        vpc = StandardVpc(
            self, 
            "MyVPC",
            cidr="10.0.0.0/16",
            max_azs=2,
        )
        
        # Create security groups
        security_groups = CommonSecurityGroups(
            self,
            "SecurityGroups",
            vpc=vpc.vpc,
        )
        
        # Allow SSH access from your IP
        security_groups.allow_management_access_from("203.0.113.0/24")  # Replace with your IP
        
        # Create an EC2 instance
        instance = StandardEC2Instance(
            self,
            "WebServer",
            vpc=vpc.vpc,
            instance_type=ec2.InstanceType("t3.micro"),
            key_name="my-key-pair",  # Replace with your key pair name
            security_group=security_groups.web_server_sg,
        )
        
        # Create an S3 bucket
        bucket = SecureS3Bucket(
            self,
            "DataBucket",
            versioned=True,
        )
        
        # Create a DynamoDB table
        table = EnhancedDynamoTable(
            self,
            "UserTable",
            partition_key=dynamodb.Attribute(
                name="userId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="sortKey",
                type=dynamodb.AttributeType.STRING
            ),
            point_in_time_recovery=True,
        )
        
        # Add a global secondary index
        table.add_global_secondary_index(
            index_name="GSI1",
            partition_key=dynamodb.Attribute(
                name="gsi1pk",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="gsi1sk",
                type=dynamodb.AttributeType.STRING
            ),
        )
        
        # Create a Lambda function
        lambda_function = LambdaFunction(
            self,
            "ProcessingFunction",
            code_path="./lambda",  # Path to your Lambda code
            handler="index.handler",
            memory_size=256,
            environment={
                "BUCKET_NAME": bucket.bucket.bucket_name,
                "TABLE_NAME": table.table.table_name,
            },
        )
        
        # Grant permissions
        bucket.grant_read_write(lambda_function.function)
        table.grant_read_write_data(lambda_function.function)
        
        # Create a serverless API
        api = ServerlessApi(
            self,
            "MyApi",
            lambda_code_path="./api",  # Path to your API code
            lambda_handler="app.handler",
            require_api_key=True,
            table_props={
                "partition_key_name": "id",
                "point_in_time_recovery": True,
            },
        )
        
        # Create a static website
        website = StaticWebsite(
            self,
            "MyWebsite",
            website_content_path="./website",  # Path to your website content
            # Uncomment to use a custom domain
            # domain_name="example.com",
            # hosted_zone_name="example.com",
        )


app = App()
ExampleStack(app, "ExampleStack")
app.synth()