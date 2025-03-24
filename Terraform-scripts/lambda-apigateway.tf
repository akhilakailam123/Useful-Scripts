data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy" "s3_policy" {
  name    = "lambda-policy"
  role    = aws_iam_role.iam_for_lambda.name

  policy = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect" : "Allow",
          "Action" : [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Resource" : "*"
        }
      ]
    }
  )
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "../Lambda-scripts/get-post-functionality.py"
  output_path = "../Lambda-scripts/get-post-functionality.zip"
}

resource "aws_lambda_function" "test_lambda" {
  filename      = "../Lambda-scripts/get-post-functionality.zip"
  function_name = "apigateway-lambda-terraform"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "get-post-functionality.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime = "python3.10"
}

resource "aws_apigatewayv2_api" "example" {
  name          = "example-http-api-terraform"
  protocol_type = "HTTP"
}

# GET Integration for /getPerson
resource "aws_apigatewayv2_integration" "get_person_integration" {
  api_id                = aws_apigatewayv2_api.example.id
  integration_type      = "AWS_PROXY"
  connection_type       = "INTERNET"
  integration_method    = "POST"  # Method must be POST for AWS_PROXY
  payload_format_version = "2.0"
  integration_uri       = aws_lambda_function.test_lambda.invoke_arn
}

# POST Integration for /createPerson
resource "aws_apigatewayv2_integration" "create_person_integration" {
  api_id                = aws_apigatewayv2_api.example.id
  integration_type      = "AWS_PROXY"
  connection_type       = "INTERNET"
  integration_method    = "POST"  # Method must be POST for AWS_PROXY
  payload_format_version = "2.0"
  integration_uri       = aws_lambda_function.test_lambda.invoke_arn
}

# GET Route for /getPerson
resource "aws_apigatewayv2_route" "get_person_route" {
  api_id    = aws_apigatewayv2_api.example.id
  route_key = "GET /getPerson"
  target    = "integrations/${aws_apigatewayv2_integration.get_person_integration.id}"
}

# POST Route for /createPerson
resource "aws_apigatewayv2_route" "create_person_route" {
  api_id    = aws_apigatewayv2_api.example.id
  route_key = "POST /createPerson"
  target    = "integrations/${aws_apigatewayv2_integration.create_person_integration.id}"
}

# Lambda permission to allow API Gateway to invoke Lambda (using the $default stage)
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.test_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.example.execution_arn}/stages/${aws_apigatewayv2_stage.example.name}/*"
}

resource "aws_lambda_permission" "apigw_lambda_post" {
  statement_id  = "AllowExecutionFromAPIGatewayPost"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.test_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.example.execution_arn}/*"
}

# Deployment resource for API Gateway
resource "aws_apigatewayv2_deployment" "example_deployment" {
  api_id = aws_apigatewayv2_api.example.id
}

# Stage resource that associates the deployment with a stage (e.g., example-stage)
resource "aws_apigatewayv2_stage" "example" {
  api_id        = aws_apigatewayv2_api.example.id
  name          = "example-stage"
  deployment_id = aws_apigatewayv2_deployment.example_deployment.id  # Make sure it's tied to the deployment
}

