
resource "aws_s3_bucket" "bucket_transformation" {
  bucket = "${var.project_name}-transformed"
  acl    = "private"
}

resource "aws_s3_bucket" "bucket_extraction" {
  bucket = "${var.project_name}-extracted"
  acl    = "private"
}