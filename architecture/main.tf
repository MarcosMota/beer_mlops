

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
  required_version = ">= 0.14.9"
}

provider "aws" {
  region  = var.region
  profile = var.profile
}

module "policies" {
  # When using these modules in your own templates, you will need to use a Git URL with a ref attribute that pins you
  # to a specific version of the modules, such as the following example:
  # source = "git::git@github.com:hashicorp/terraform-aws-consul.git//modules/consul-cluster?ref=v0.0.1"
  source = "./modules/policies"
}


module "storage" {
  # When using these modules in your own templates, you will need to use a Git URL with a ref attribute that pins you
  # to a specific version of the modules, such as the following example:
  # source = "git::git@github.com:hashicorp/terraform-aws-consul.git//modules/consul-cluster?ref=v0.0.1"
  source = "./modules/storage"
  project_name = "beer"
}

data "archive_file" "fn_extraction_zip" {
  type        = "zip"
  output_path = "dist/fn_extraction.zip"
  source_dir = var.fn_extraction_path
}

data "archive_file" "fn_transform_zip" {
  type        = "zip"
  output_path = "dist/fn_transform.zip"
  source_dir = var.fn_transform_path
}

module "data_ingestion" {
  # When using these modules in your own templates, you will need to use a Git URL with a ref attribute that pins you
  # to a specific version of the modules, such as the following example:
  # source = "git::git@github.com:hashicorp/terraform-aws-consul.git//modules/consul-cluster?ref=v0.0.1"
  source = "./modules/data_ingestion"
  project_name = var.project_name
  region = var.region
  fn_transform = {
    name = "fn_transform"
    path = data.archive_file.fn_transform_zip.output_path
  }

  fn_extraction = {
    name = "fn_extraction"
    path = data.archive_file.fn_extraction_zip.output_path
  }

  bucket_extraction_arn = module.storage.bucket_extraction_arn
  bucket_transform_arn = module.storage.bucket_transform_arn

  role = {
    lambda_arn = module.policies.iam_lambda_role
    lambda_name = module.policies.name_lambda_role
    firehouse_arn = module.policies.iam_firehouse_role
  }
}

module "modelling" {
  source = "./modules/modeling"
  role_sagemake_arn = module.policies.iam_sagemaker_role
  profile = var.profile
}
