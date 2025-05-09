from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
)
from ..compute import LambdaFunction
from ..database import EnhancedDynamoTable


class ServerlessApi(Construct):
    """
    A complete serverless API pattern with API Gateway, Lambda, and DynamoDB.
    
    Features:
    - REST API with API Gateway
    - Lambda function for backend processing
    - DynamoDB table for data storage
    - Proper IAM permissions
    - CORS configuration
    - API key (optional)
    """
    
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        lambda_code_path: str,
        lambda_handler: str = "index.handler",
        api_name: str = None,
        enable_cors: bool = True,
        require_api_key: bool = False,
        table_props: dict = None,
        **kwargs
    ):
        super().__init__(scope, id)
        
        # Create DynamoDB table
        table_props = table_props or {}
        self.table = EnhancedDynamoTable(
            self,
            "Table",
            partition_key=dynamodb.Attribute(
                name=table_props.get("partition_key_name", "id"),
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=table_props.get("sort_key") or None,
            **{k: v for k, v in table_props.items() if k not in ["partition_key_name", "sort_key"]}
        )
        
        # Create Lambda function
        self.function = LambdaFunction(
            self,
            "Function",
            code_path=lambda_code_path,
            handler=lambda_handler,
            environment={
                "TABLE_NAME": self.table.table.table_name,
            },
        )
        
        # Grant Lambda function access to DynamoDB table
        self.table.table.grant_read_write_data(self.function.function)
        
        # Create API Gateway
        api_props = {
            "rest_api_name": api_name or f"{id}-api",
            "description": f"API for {id}",
        }
        
        if require_api_key:
            api_props["api_key_required"] = True
        
        self.api = apigw.LambdaRestApi(
            self,
            "Api",
            handler=self.function.function,
            proxy=True,
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ) if enable_cors else None,
            **api_props
        )
        
        if require_api_key:
            plan = self.api.add_usage_plan("UsagePlan",
                name=f"{id}-usage-plan",
                throttle=apigw.ThrottleSettings(
                    rate_limit=10,
                    burst_limit=20
                )
            )
            key = self.api.add_api_key("ApiKey")
            plan.add_api_key(key)
            plan.add_api_stage(
                stage=self.api.deployment_stage
            )
            
        # Export outputs
        self.api_endpoint = self.api.url
        self.table_name = self.table.table.table_name