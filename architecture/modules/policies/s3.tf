resource "aws_iam_role_policy_attachment" "s3-full-acess-policy-attachment" {
    role = aws_iam_role.firehose_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
