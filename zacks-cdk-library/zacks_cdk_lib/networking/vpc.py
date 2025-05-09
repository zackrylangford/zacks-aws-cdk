from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    Tags,
)


class StandardVpc(Construct):
    """
    A standardized VPC with best practices for security and availability.
    
    Features:
    - Public and private subnets across multiple AZs
    - NAT gateways for private subnet internet access
    - VPC flow logs
    - Network ACLs
    - Standard CIDR allocation
    """
    
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        cidr: str = "10.0.0.0/16",
        max_azs: int = 2,
        nat_gateways: int = 1,
        enable_flow_logs: bool = True,
        subnet_configuration: list = None,
        **kwargs
    ):
        super().__init__(scope, id)
        
        # Define default subnet configuration if not provided
        if subnet_configuration is None:
            subnet_configuration = [
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="Isolated",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24,
                ),
            ]
        
        # Create the VPC
        self.vpc = ec2.Vpc(
            self,
            "VPC",
            cidr=cidr,
            max_azs=max_azs,
            nat_gateways=nat_gateways,
            subnet_configuration=subnet_configuration,
            **kwargs
        )
        
        # Add flow logs if enabled
        if enable_flow_logs:
            self.vpc.add_flow_log("FlowLog")
        
        # Add standard tags
        Tags.of(self.vpc).add("Name", f"{id}-vpc")
    
    def add_interface_endpoint(self, service_name: str, subnets=None):
        """Add a VPC interface endpoint for the specified service"""
        return self.vpc.add_interface_endpoint(
            f"{service_name.split('.')[-1]}Endpoint",
            service=ec2.InterfaceVpcEndpointAwsService(service_name),
            subnets=subnets,
        )
    
    def add_gateway_endpoint(self, service: ec2.GatewayVpcEndpointAwsService, subnets=None):
        """Add a VPC gateway endpoint for the specified service"""
        return self.vpc.add_gateway_endpoint(
            f"{service.name}Endpoint",
            service=service,
            subnets=subnets,
        )