from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    aws_kms as kms,
    RemovalPolicy,
)


class SecureS3Bucket(Construct):
    """
    A secure S3 bucket with best practices for security and compliance.
    
    Features:
    - Server-side encryption with KMS (optional)
    - Versioning enabled
    - Public access blocked
    - Lifecycle rules for cost optimization
    - Access logging (optional)
    """
    
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        bucket_name: str = None,
        encryption_key: kms.IKey = None,
        versioned: bool = True,
        enforce_ssl: bool = True,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        auto_delete_objects: bool = False,
        lifecycle_rules: list = None,
        enable_access_logging: bool = False,
        **kwargs
    ):
        super().__init__(scope, id)
        
        # Create a KMS key if encryption is requested but no key provided
        if encryption_key is None:
            encryption = s3.BucketEncryption.S3_MANAGED
            encryption_key = None
        else:
            encryption = s3.BucketEncryption.KMS
        
        # Create the bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            "Bucket",
            bucket_name=bucket_name,
            encryption=encryption,
            encryption_key=encryption_key,
            versioned=versioned,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=enforce_ssl,
            removal_policy=removal_policy,
            auto_delete_objects=auto_delete_objects,
            **kwargs
        )
        
        # Add lifecycle rules if provided
        if lifecycle_rules:
            for rule in lifecycle_rules:
                self.bucket.add_lifecycle_rule(**rule)
        else:
            # Add default lifecycle rule to move objects to Infrequent Access after 90 days
            self.bucket.add_lifecycle_rule(
                transitions=[
                    s3.Transition(
                        storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                        transition_after=Duration.days(90)
                    )
                ]
            )
        
        # Set up access logging if requested
        if enable_access_logging:
            log_bucket = s3.Bucket(
                self,
                "LogBucket",
                encryption=encryption,
                encryption_key=encryption_key,
                block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                enforce_ssl=enforce_ssl,
                removal_policy=removal_policy,
            )
            self.bucket.enable_access_logging(log_bucket)
            self.log_bucket = log_bucket
    
    def grant_read(self, identity):
        """Grant read permissions to the given identity"""
        return self.bucket.grant_read(identity)
    
    def grant_write(self, identity):
        """Grant write permissions to the given identity"""
        return self.bucket.grant_write(identity)
    
    def grant_read_write(self, identity):
        """Grant read and write permissions to the given identity"""
        return self.bucket.grant_read_write(identity)