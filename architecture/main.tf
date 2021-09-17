

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
  # Gerencia todas as policies e roles da arquitetura
  source = "./modules/policies"
  region = var.region
}


module "storage" {
  # Gerencia recursos de storage, como S3 e Glue Table 
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
  # Gerencia recursos de ingestão de dados, como Kinesis Stream e Firehose
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
    glue_arn = module.policies.iam_glue_role
  }
}

module "machine_learning" {
  # Gerencia recursos de storage, como S3 e Glue Table 
  source = "./modules/machine_learning"
  role_sagemake_arn = module.policies.iam_sagemaker_role
  project_name = var.project_name
  repository_url = "https://github.com/MarcosMota/beer_mlops.git"
  profile = var.profile
}
