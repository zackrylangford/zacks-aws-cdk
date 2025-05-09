from constructs import Construct
from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
)


class EnhancedDynamoTable(Construct):
    """
    An enhanced DynamoDB table with common configurations and best practices.
    
    Features:
    - Configurable capacity (on-demand by default)
    - Point-in-time recovery
    - Auto-scaling (for provisioned capacity)
    - TTL support
    - Stream configuration
    - Global secondary indexes
    """
    
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        table_name: str = None,
        partition_key: dynamodb.Attribute,
        sort_key: dynamodb.Attribute = None,
        billing_mode: dynamodb.BillingMode = dynamodb.BillingMode.PAY_PER_REQUEST,
        read_capacity: int = None,
        write_capacity: int = None,
        point_in_time_recovery: bool = True,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        stream: dynamodb.StreamViewType = None,
        ttl_attribute: str = None,
        global_indexes: list = None,
        **kwargs
    ):
        super().__init__(scope, id)
        
        # Create the DynamoDB table
        self.table = dynamodb.Table(
            self,
            "Table",
            table_name=table_name,
            partition_key=partition_key,
            sort_key=sort_key,
            billing_mode=billing_mode,
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            point_in_time_recovery=point_in_time_recovery,
            removal_policy=removal_policy,
            stream=stream,
            **kwargs
        )
        
        # Configure TTL if specified
        if ttl_attribute:
            self.table.add_time_to_live_attribute(ttl_attribute)
        
        # Add global secondary indexes if provided
        if global_indexes:
            for index in global_indexes:
                self.table.add_global_secondary_index(**index)
    
    def add_global_secondary_index(
        self,
        index_name: str,
        partition_key: dynamodb.Attribute,
        sort_key: dynamodb.Attribute = None,
        read_capacity: int = None,
        write_capacity: int = None,
        projection_type: dynamodb.ProjectionType = dynamodb.ProjectionType.ALL,
        non_key_attributes: list = None,
    ):
        """Add a global secondary index to the table"""
        self.table.add_global_secondary_index(
            index_name=index_name,
            partition_key=partition_key,
            sort_key=sort_key,
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            projection_type=projection_type,
            non_key_attributes=non_key_attributes,
        )
        return self
    
    def grant_read_data(self, identity):
        """Grant read permissions to the given identity"""
        return self.table.grant_read_data(identity)
    
    def grant_write_data(self, identity):
        """Grant write permissions to the given identity"""
        return self.table.grant_write_data(identity)
    
    def grant_read_write_data(self, identity):
        """Grant read and write permissions to the given identity"""
        return self.table.grant_read_write_data(identity)