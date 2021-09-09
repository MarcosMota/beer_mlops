
resource "aws_iam_role_policy_attachment" "glue-full-acess-policy-attachment" {
    role = aws_iam_role.firehose_role.name
    policy_arn = "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
}

