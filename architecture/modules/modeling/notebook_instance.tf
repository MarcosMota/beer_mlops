
resource "aws_sagemaker_code_repository" "code_repository" {
  code_repository_name = "my-notebook-instance-code-repo"

  git_config {
    repository_url = "https://github.com/MarcosMota/beer_mlops.git"
  }
}

resource "aws_sagemaker_notebook_instance" "notebook_instance" {
  name                    = "my-notebook-instance"
  role_arn                = var.role_sagemake_arn
  instance_type           = var.instance_type
  default_code_repository = aws_sagemaker_code_repository.code_repository.code_repository_name
}