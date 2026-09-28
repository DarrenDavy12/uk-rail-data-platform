# Defines configurable values.

# region
# bucket name
# environment


variable "aws_region" {
  description = "AWS region for the project"
  type        = string
  default     = "eu-west-2"
}

variable "bucket_name" {
  description = "S3 bucket name for the rail data platform"
  type        = string
}


