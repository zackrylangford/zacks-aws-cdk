from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
)


class CommonSecurityGroups(Construct):
    """
    A collection of commonly used security groups with predefined rules.
    
    Features:
    - Web server security group (HTTP/HTTPS)
    - Database security group
    - Application server security group
    - Management security group (SSH/RDP)
    """
    
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc: ec2.IVpc,
    ):
        super().__init__(scope, id)
        
        # Web server security group (HTTP/HTTPS)
        self.web_server_sg = ec2.SecurityGroup(
            self,
            "WebServerSG",
            vpc=vpc,
            description="Security group for web servers",
            allow_all_outbound=True,
        )
        self.web_server_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow HTTP traffic"
        )
        self.web_server_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow HTTPS traffic"
        )
        
        # Database security group
        self.database_sg = ec2.SecurityGroup(
            self,
            "DatabaseSG",
            vpc=vpc,
            description="Security group for databases",
            allow_all_outbound=True,
        )
        # Allow access from web server security group
        self.database_sg.add_ingress_rule(
            self.web_server_sg,
            ec2.Port.tcp(3306),
            "Allow MySQL traffic from web servers"
        )
        self.database_sg.add_ingress_rule(
            self.web_server_sg,
            ec2.Port.tcp(5432),
            "Allow PostgreSQL traffic from web servers"
        )
        
        # Application server security group
        self.app_server_sg = ec2.SecurityGroup(
            self,
            "AppServerSG",
            vpc=vpc,
            description="Security group for application servers",
            allow_all_outbound=True,
        )
        # Allow access from web server security group
        self.app_server_sg.add_ingress_rule(
            self.web_server_sg,
            ec2.Port.tcp_range(8000, 9000),
            "Allow application traffic from web servers"
        )
        
        # Management security group (SSH/RDP)
        self.management_sg = ec2.SecurityGroup(
            self,
            "ManagementSG",
            vpc=vpc,
            description="Security group for management access",
            allow_all_outbound=True,
        )
        # By default, no ingress rules - add specific IPs as needed
    
    def allow_management_access_from(self, ip_or_cidr: str):
        """Allow SSH and RDP access from the specified IP or CIDR"""
        self.management_sg.add_ingress_rule(
            ec2.Peer.ipv4(ip_or_cidr),
            ec2.Port.tcp(22),
            f"Allow SSH from {ip_or_cidr}"
        )
        self.management_sg.add_ingress_rule(
            ec2.Peer.ipv4(ip_or_cidr),
            ec2.Port.tcp(3389),
            f"Allow RDP from {ip_or_cidr}"
        )
        return self