
resource "aws_s3_bucket" "bucket_transformation" {
  bucket = "${var.project_name}-transformed"
  acl    = "private"
  force_destroy = true

}

resource "aws_s3_bucket" "bucket_extraction" {
  bucket = "${var.project_name}-extracted"
  acl    = "private"
  force_destroy = true
}


