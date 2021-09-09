output "bucket_extraction_arn" {
  value = aws_s3_bucket.bucket_extraction.arn
}

output "bucket_transform_arn" {
  value = aws_s3_bucket.bucket_transformation.arn
}