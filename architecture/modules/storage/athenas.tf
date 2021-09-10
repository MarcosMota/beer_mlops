resource "aws_athena_database" "this" {
  name   = "${var.project_name}_db"
  bucket = aws_s3_bucket.bucket_athena.bucket
}