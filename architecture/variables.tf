variable "project_name" {
    default = "beer"
    type = string
    description = "Nome do projeto"
}
variable "profile" {
    default = "marcosmota"
  type = string
}

variable "region" {
  default = "us-east-1"
}

variable "fn_extraction_path" {
    default = "marcosmota"
    type = string
    description = "Caminho da função de extração"
}

variable "fn_transform_path" {
    type = string
    description = "Caminho da função de transformação"
}

variable "environment" {
    type = string
    description = "Ambiente"
    default = "dev"
}
