
resource "aws_iam_role_policy_attachment" "glue-full-acess-policy-attachment" {
  role       = aws_iam_role.firehose_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
}

resource "aws_iam_role" "glue_role" {
  name = "glue_role"
  assume_role_policy = jsonencode(
 {
    "Version": "2012-10-17",
    "Statement": [
    {
        "Action": "sts:AssumeRole",
        "Principal": {
        "Service": "glue.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
    }
    ]
 })
}