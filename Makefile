


# Commands terraform

project-install:
	pip install -r requirements.txt

project-test:
	echo 'iniciando teste'
	python -m unittest -v

arch-init: 
	terraform -chdir=./architecture init

arch-plan: 
	terraform -chdir=./architecture plan

arch-apply: 
	terraform -chdir=./architecture apply -auto-approve

arch-destroy: 
	terraform -chdir=./architecture destroy -auto-approve

