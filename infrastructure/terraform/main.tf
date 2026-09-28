# Defines the actual AWS resources.

# "Create an S3 bucket in aws"

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "rail_data" {
  bucket = var.bucket_name

  tags = {
    Project     = "UK Rail Data Platform"
    Environment = "Development"
    ManagedBy   = "Terraform"
  }
}


