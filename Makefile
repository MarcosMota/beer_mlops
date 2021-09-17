

terraform-init: 
	terraform -chdir=./architecture init

terraform-plan: 
	terraform -chdir=./architecture plan

terraform-apply: 
	terraform -chdir=./architecture apply -auto-approve

terraform-destroy: 
	terraform -chdir=./architecture destroy -auto-approve