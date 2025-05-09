# Zack's AWS CDK Library

A collection of reusable AWS CDK constructs for quickly provisioning and managing cloud resources using Python.

## Overview

This repository contains a custom AWS CDK library that provides:

- Higher-level abstractions for common AWS resources
- Pre-configured best practices for security and scalability
- Reusable patterns for common architectures
- Simplified API for faster development

## Installation

```bash
# Clone the repository
git clone https://github.com/zackrylangford/zacks-cdk-library.git

# Install the library in development mode
cd zacks-cdk-library
pip install -e .
```

## Library Structure

- `zacks_cdk_lib/compute/` - Compute resources (Lambda, EC2)
- `zacks_cdk_lib/storage/` - Storage resources (S3, EFS)
- `zacks_cdk_lib/database/` - Database resources (DynamoDB, RDS)
- `zacks_cdk_lib/networking/` - Networking resources (VPC, subnets)
- `zacks_cdk_lib/security/` - Security resources (IAM, Security Groups)
- `zacks_cdk_lib/patterns/` - Higher-level architectural patterns

## Usage Example

```python
from aws_cdk import App, Stack
from constructs import Construct
from zacks_cdk_lib.compute import LambdaFunction
from zacks_cdk_lib.storage import SecureS3Bucket
from zacks_cdk_lib.patterns import ServerlessApi

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
```

## Prerequisites

- Python 3.6+
- AWS CDK v2
- AWS CLI configured with appropriate credentials

## License

This project is licensed under the MIT License - see the LICENSE file for details.