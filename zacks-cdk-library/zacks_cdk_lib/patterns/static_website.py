from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    RemovalPolicy,
)
from ..storage import SecureS3Bucket


class StaticWebsite(Construct):
    """
    A complete static website pattern with S3, CloudFront, and optional Route53.
    
    Features:
    - S3 bucket for static content
    - CloudFront distribution with HTTPS
    - Custom domain with ACM certificate (optional)
    - Route53 DNS records (optional)
    - Content deployment from local directory
    """
    
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        website_content_path: str = None,
        domain_name: str = None,
        hosted_zone_id: str = None,
        hosted_zone_name: str = None,
        index_document: str = "index.html",
        error_document: str = "error.html",
        **kwargs
    ):
        super().__init__(scope, id)
        
        # Create S3 bucket for website content
        self.bucket = SecureS3Bucket(
            self,
            "WebsiteBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        
        # Configure CloudFront distribution
        certificate = None
        domain_names = None
        
        # If domain name is provided, create ACM certificate
        if domain_name:
            if hosted_zone_id or hosted_zone_name:
                # Look up the hosted zone
                if hosted_zone_id:
                    hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
                        self,
                        "HostedZone",
                        hosted_zone_id=hosted_zone_id,
                        zone_name=hosted_zone_name or domain_name.split(".", 1)[1]
                    )
                else:
                    hosted_zone = route53.HostedZone.from_lookup(
                        self,
                        "HostedZone",
                        domain_name=hosted_zone_name
                    )
                
                # Create ACM certificate
                certificate = acm.Certificate(
                    self,
                    "Certificate",
                    domain_name=domain_name,
                    validation=acm.CertificateValidation.from_dns(hosted_zone)
                )
                
                domain_names = [domain_name]
        
        # Create CloudFront distribution
        self.distribution = cloudfront.Distribution(
            self,
            "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(self.bucket.bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            ),
            default_root_object=index_document,
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path=f"/{error_document}",
                )
            ],
            certificate=certificate,
            domain_names=domain_names,
        )
        
        # Create Route53 record if domain name and hosted zone are provided
        if domain_name and (hosted_zone_id or hosted_zone_name):
            route53.ARecord(
                self,
                "AliasRecord",
                zone=hosted_zone,
                record_name=domain_name,
                target=route53.RecordTarget.from_alias(
                    targets.CloudFrontTarget(self.distribution)
                )
            )
        
        # Deploy website content if path is provided
        if website_content_path:
            s3deploy.BucketDeployment(
                self,
                "DeployWebsite",
                sources=[s3deploy.Source.asset(website_content_path)],
                destination_bucket=self.bucket.bucket,
                distribution=self.distribution,
                distribution_paths=["/*"],
            )
        
        # Export outputs
        self.bucket_name = self.bucket.bucket.bucket_name
        self.distribution_domain_name = self.distribution.distribution_domain_name
        self.distribution_id = self.distribution.distribution_id