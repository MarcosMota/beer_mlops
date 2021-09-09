resource "aws_cloudwatch_event_rule" "every_five_minutes" {
    name = "extraction-schedule"
    description = "Fires every five minutes"
    schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "scheduler" {
    rule = aws_cloudwatch_event_rule.every_five_minutes.name
    target_id = aws_lambda_function.lambda_extraction.function_name
    arn = aws_lambda_function.lambda_extraction.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = var.fn_extraction.name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.every_five_minutes.arn
}

resource "aws_cloudwatch_log_group" "fn_transform_log_group" {
  name              = "/aws/lambda/${var.fn_transform.name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "fn_extraction_log_group" {
  name              = "/aws/lambda/${var.fn_extraction.name}"
  retention_in_days = 14
}



