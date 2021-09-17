# Arquitetura do Terraform

## Variaveis

Neste projeto utilizamos o arquivo `dev.auto.tfvars` para criar um ambiente de desenvolvimento e o arquivo `prod.auto.tfvars` gerenciar o ambiente de produção.

A estrutura do arquivo de variáveis deverá ser da seguinte forma.

```
project_name = "beer"
fn_extraction_path = "../src/lambda/extraction"
fn_transform_path = "../src/lambda/transform"
environment = "dev"
profile = "marcosmota"
```

- __fn_extraction_path:__ Pasta da função de extração
- __fn_transform_path:__ Pasta da função de transformação
- __environment:__ Variável de ambiente (dev, test)
- __profile:__ profile

## Modulos
A arquitetura do Terraform desse projeto é separada em modulos, sendo

- __data_ingestion:__ Recursos de ingestão de dados, como Kinesis Stream e Firehose
- __machine_learning:__ Recursos de Machine Learning, como Sage Maker
- __policies:__ Gerencia todas as policies e roles da arquitetura
- __storage:__ Recursos de storage, como S3 e Glue Table