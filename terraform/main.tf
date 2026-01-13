provider "aws" {
  region = "us-east-1"
}

resource "random_id" "suffix" {
  byte_length = 2
}

resource "aws_s3_bucket" "cost_data" {
  bucket = "cost-ai-data-${random_id.suffix.hex}"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../scripts/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_iam_role" "lambda_exec" {
  name = "cost_optimizer_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "cost_optimizer_policy"
  role = aws_iam_role.lambda_exec.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Action = ["ce:GetCostAndUsage"], Effect = "Allow", Resource = "*" },
      { Action = ["s3:PutObject"], Effect = "Allow", Resource = "${aws_s3_bucket.cost_data.arn}/*" },
      { Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Effect = "Allow", Resource = "*" }
    ]
  })
}

# Attach SNS Permission
resource "aws_iam_role_policy_attachment" "sns_access" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
}

resource "aws_sns_topic" "cost_alert" {
  name = "cost-threshold-alert"
}

resource "aws_sns_topic_subscription" "email_target" {
  topic_arn = aws_sns_topic.cost_alert.arn
  protocol  = "email"
  endpoint  = "haharshsingh57@gmail.com"
}

resource "aws_lambda_function" "cost_harvester" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "cost_harvester_api"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 30

  environment {
    variables = {
      BUCKET_NAME   = aws_s3_bucket.cost_data.id
      SNS_TOPIC_ARN = aws_sns_topic.cost_alert.arn
    }
  }
}

output "lambda_name" { value = aws_lambda_function.cost_harvester.function_name }
output "bucket_name" { value = aws_s3_bucket.cost_data.id }