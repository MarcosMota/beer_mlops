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