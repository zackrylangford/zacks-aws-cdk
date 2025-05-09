from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_logs as logs,
    Duration,
    RemovalPolicy,
)


class LambdaFunction(Construct):
    """
    A custom Lambda function construct with sensible defaults and additional features.
    
    Features:
    - Configurable memory and timeout
    - Log retention settings
    - Dead letter queue support (optional)
    - Environment variables
    - VPC configuration (optional)
    """
    
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        code_path: str,
        handler: str = "index.handler",
        runtime: _lambda.Runtime = _lambda.Runtime.PYTHON_3_9,
        memory_size: int = 128,
        timeout: Duration = Duration.seconds(30),
        environment: dict = None,
        log_retention: logs.RetentionDays = logs.RetentionDays.ONE_WEEK,
        description: str = None,
        **kwargs
    ):
        super().__init__(scope, id)
        
        # Create the Lambda function with provided parameters
        self.function = _lambda.Function(
            self,
            "Function",
            runtime=runtime,
            handler=handler,
            code=_lambda.Code.from_asset(code_path),
            memory_size=memory_size,
            timeout=timeout,
            environment=environment or {},
            description=description or f"Lambda function created with my-cdk-lib",
            log_retention=log_retention,
            **kwargs
        )
        
        # Store the function as a public property
        self.lambda_function = self.function
    
    def add_environment_variable(self, key: str, value: str):
        """Add an environment variable to the Lambda function"""
        self.function.add_environment(key, value)
        return self
    
    def grant_invoke(self, identity):
        """Grant invoke permissions to the given identity"""
        self.function.grant_invoke(identity)
        return self