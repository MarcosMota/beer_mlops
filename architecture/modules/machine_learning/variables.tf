
variable "region" {
  type = string
}

variable "profile" {
  type = string
}

variable "role_sagemake_arn" {
  type = string
}

variable "instance_type" {
  type = string
  default = "ml.t2.medium"
}
variable "project_name" {
    type = string
    description = "Nome do projeto"
}

variable "repository_url" {
    type = string
    description = "Repositório Github do projeto"
}