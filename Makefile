

# Get the latest tag
TAG=$(shell git describe --tags --abbrev=0)
GIT_COMMIT=$(shell git log -1 --format=%h)
AWS_ACCOUNT=178520105998
TERRAFORM_VERSION=0.12.28

terraform-init: ## Run terraform init to download all necessary plugins
	  docker run --rm -v $$PWD:/app -v $$HOME/.ssh/:/root/.ssh/ -w /app/ -e AWS_ACCESS_KEY_ID=$$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$$AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION=$$AWS_DEFAULT_REGION -e TF_VAR_APP_VERSION=$(GIT_COMMIT) hashicorp/terraform:$(TERRAFORM_VERSION) init -upgrade=true
