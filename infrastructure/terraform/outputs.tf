# Tells us useful information after Terraform creates infrastructure.

# bucket name
# bucket ARN



output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.rail_data.bucket
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.rail_data.arn
}


