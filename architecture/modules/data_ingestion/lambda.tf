
resource "aws_lambda_function" "lambda_extraction" {
  filename      = var.fn_extraction.path
  function_name = var.fn_extraction.name
  role          = var.role.lambda_arn
  handler       = "fn_extraction.handler"
  source_code_hash = filebase64sha256(var.fn_extraction.path)
  runtime = "python3.7"
  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.fn_extraction_log_group,
  ]

  environment {
    variables = {
      PROJECT_STEAM = aws_kinesis_stream.kinesis_stream.name
    }
  }
}

resource "aws_lambda_function" "lambda_transform" {
  filename      = var.fn_transform.path
  function_name = var.fn_transform.name
  role          = var.role.lambda_arn
  handler       = "fn_transform.handler"
  source_code_hash = filebase64sha256(var.fn_transform.path)
  runtime = "python3.7"
   depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.fn_transform_log_group,
  ]
}
resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = var.role.lambda_name
  policy_arn = aws_iam_policy.lambda_logging.arn
}