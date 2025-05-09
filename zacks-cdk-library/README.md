# Zack's CDK Library

A collection of reusable AWS CDK constructs for quickly provisioning cloud resources.

## Installation

```
pip install -e .
```

## Usage

```python
from zacks_cdk_lib.compute import LambdaFunction
from zacks_cdk_lib.storage import SecureS3Bucket
from zacks_cdk_lib.database import EnhancedDynamoTable

# Use your custom constructs in your CDK stack
```