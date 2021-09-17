
resource "aws_s3_bucket" "bucket_transformation" {
  bucket = "transformed"
  acl    = "private"
  force_destroy = true

}

resource "aws_s3_bucket" "bucket_extraction" {
  bucket = "cleaned"
  acl    = "private"
  force_destroy = true
}


