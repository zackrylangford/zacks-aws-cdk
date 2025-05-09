# My Personal AWS CDK Library

A collection of reusable AWS CDK constructs for quickly provisioning and managing cloud resources using Python.

## Overview

This repository contains a custom AWS CDK library that provides:

- Higher-level abstractions for common AWS resources
- Pre-configured best practices for security and scalability
- Reusable patterns for common architectures
- Simplified API for faster development

## Getting Started

### Prerequisites

- Python 3.6+
- AWS CDK v2
- AWS CLI configured with appropriate credentials

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/my-cdk-lib.git
   ```

2. Install the library in development mode:
   ```
   cd my-cdk-lib
   pip install -e .
   ```

3. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

## Library Structure

- `my_cdk_lib/compute/` - Compute resources (Lambda, EC2)
- `my_cdk_lib/storage/` - Storage resources (S3, EFS)
- `my_cdk_lib/database/` - Database resources (DynamoDB, RDS)
- `my_cdk_lib/networking/` - Networking resources (VPC, subnets)
- `my_cdk_lib/security/` - Security resources (IAM, Security Groups)
- `my_cdk_lib/patterns/` - Higher-level architectural patterns

## Usage Examples

See `example_usage.py` for a complete example of how to use this library.

### Basic Example

```python
from aws_cdk import App, Stack
from constructs import Construct
from my_cdk_lib.compute import LambdaFunction
from my_cdk_lib.storage import SecureS3Bucket
from my_cdk_lib.patterns import ServerlessApi

class MyStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create a secure S3 bucket
        bucket = SecureS3Bucket(
            self,
            "MyBucket",
            versioned=True,
        )
        
        # Create a Lambda function
        lambda_fn = LambdaFunction(
            self,
            "MyFunction",
            code_path="./lambda",
            handler="index.handler",
        )
        
        # Grant the Lambda function access to the bucket
        bucket.grant_read_write(lambda_fn.function)
        
        # Create a serverless API
        api = ServerlessApi(
            self,
            "MyApi",
            lambda_code_path="./api",
            lambda_handler="app.handler",
        )

app = App()
MyStack(app, "MyStack")
app.synth()
```

## Contributing

Feel free to extend this library with additional constructs and patterns as needed for your projects.

## License

This project is licensed under the MIT License - see the LICENSE file for details.