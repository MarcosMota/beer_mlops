output "iam_lambda_role" {
  value = aws_iam_role.lambda_role.arn
}

output "iam_sagemaker_role" {
  value = aws_iam_role.sagemaker_role.arn
}

output "name_lambda_role" {
  value = aws_iam_role.lambda_role.name
}

output "iam_firehouse_role" {
  value = aws_iam_role.firehose_role.arn
}
