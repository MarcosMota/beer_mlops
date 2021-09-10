
variable "role" {
  type = object({
    lambda_arn = string
    lambda_name = string
    firehouse_arn = string
    glue_arn = string
  })
}

variable "bucket_transform_arn" {
  type = string
}

variable "bucket_extraction_arn" {
  type = string
}

variable "region" {
  type = string
}

variable "project_name" {
  type = string
}
variable "profile" {
    default = "marcosmota"
  type = string
}

variable "fn_extraction" {
  type = object({
    name = string
    path = string
  })
  description = "Informações sobre a função lambda de extração"
}

variable "fn_transform" {
  type = object({
    name = string
    path = string
  })
  description = "Informações sobre a função lambda de limpeza"
}