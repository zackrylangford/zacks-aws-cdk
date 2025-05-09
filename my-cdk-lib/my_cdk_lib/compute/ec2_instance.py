from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Tags,
)


class StandardEC2Instance(Construct):
    """
    A standardized EC2 instance with common configurations and best practices.
    
    Features:
    - Amazon Linux 2 by default
    - SSM enabled for management
    - Security group with common rules
    - Instance profile with common permissions
    """
    
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        vpc: ec2.IVpc,
        instance_type: ec2.InstanceType = ec2.InstanceType("t3.micro"),
        machine_image: ec2.IMachineImage = None,
        key_name: str = None,
        user_data: ec2.UserData = None,
        security_group: ec2.SecurityGroup = None,
        role: iam.Role = None,
        subnet_selection: ec2.SubnetSelection = None,
        **kwargs
    ):
        super().__init__(scope, id)
        
        # Use Amazon Linux 2 by default if no image is specified
        if machine_image is None:
            machine_image = ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                edition=ec2.AmazonLinuxEdition.STANDARD,
                virtualization=ec2.AmazonLinuxVirt.HVM,
                storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            )
        
        # Create a security group if not provided
        if security_group is None:
            security_group = ec2.SecurityGroup(
                self, 
                "SecurityGroup",
                vpc=vpc,
                description=f"Security group for {id}",
                allow_all_outbound=True,
            )
            
            # Add SSH access if key_name is provided
            if key_name:
                security_group.add_ingress_rule(
                    ec2.Peer.any_ipv4(),
                    ec2.Port.tcp(22),
                    "Allow SSH access"
                )
        
        # Create a role with SSM permissions if not provided
        if role is None:
            role = iam.Role(
                self, 
                "InstanceRole",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            )
            role.add_managed_policy(
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                )
            )
        
        # Create the EC2 instance
        self.instance = ec2.Instance(
            self,
            "Instance",
            vpc=vpc,
            instance_type=instance_type,
            machine_image=machine_image,
            key_name=key_name,
            user_data=user_data,
            security_group=security_group,
            role=role,
            vpc_subnets=subnet_selection or ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            **kwargs
        )
        
        # Add standard tags
        Tags.of(self.instance).add("ManagedBy", "CDK")
        
    def add_security_group_rule(self, peer, port, description=None):
        """Add an ingress rule to the instance's security group"""
        self.instance.connections.allow_from(peer, port, description)
        return self