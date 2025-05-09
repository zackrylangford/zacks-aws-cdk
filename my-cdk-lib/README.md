# My Personal CDK Library

A collection of reusable AWS CDK constructs for quickly provisioning cloud resources.

## Installation

```
pip install -e .
```

## Usage

```python
from my_cdk_lib.compute import LambdaFunction
from my_cdk_lib.storage import S3Bucket
from my_cdk_lib.database import DynamoTable

# Use your custom constructs in your CDK stack
```