
resource "random_string" "resource_code" {
  length  = 5
  special = false
  upper   = false
}

resource "aws_s3_bucket" "bucket_transformation" {
  bucket = "transformed-${random_string.resource_code.result}"
  acl    = "private"
  force_destroy = true
}

resource "aws_s3_bucket" "bucket_extraction" {
  bucket = "cleaned-${random_string.resource_code.result}"
  acl    = "private"
  force_destroy = true
}


resource "aws_s3_bucket" "bucket_dataset" {
  bucket = "dataset-${random_string.resource_code.result}"
  acl    = "private"
  force_destroy = true
}


