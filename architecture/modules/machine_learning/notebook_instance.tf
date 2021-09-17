resource "aws_sagemaker_code_repository" "code_repository" {
  code_repository_name = "${var.project_name}-instance-code-repo"

  git_config {
    repository_url = var.repository_url
  }
}

resource "aws_sagemaker_notebook_instance" "notebook_instance" {
  name                    = "${var.project_name}-notebook-instance"
  role_arn                = var.role_sagemake_arn
  instance_type           = var.instance_type
  default_code_repository = aws_sagemaker_code_repository.code_repository.code_repository_name
}