module "function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.8.1"

  create_function = var.create
  create_package  = var.create_package
  create_role     = var.create

  function_name = "${var.name_prefix}-expired-account-monitor"
  description   = "List users that haven't logged in within the maximum allowed time limit"
  handler       = "src/lambda_handler.handle_event"
  runtime       = "python3.11"
  timeout       = 30

  attach_policy_json = var.create
  policy_json        = var.create ? data.aws_iam_policy_document.function[0].json : null

  source_path = [
    {
      path           = "${path.module}/function"
      patterns       = ["!tests/.*"]
      poetry_install = true
    }
  ]

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-expired-account-monitor"
    }
  )
}

data "aws_iam_policy_document" "function" {
  count = var.create ? 1 : 0

  statement {
    effect = "Allow"

    actions = [
      "iam:GenerateCredentialReport",
      "iam:GetCredentialReport",
    ]

    resources = [
      "*"
    ]
  }
}

data "aws_iam_policy_document" "service_role" {
  count = var.create ? 1 : 0

  statement {
    sid    = "AllowOidcToExecuteExpiryFunction"
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction"
    ]

    resources = [
      module.function.lambda_function_arn
    ]
  }
}

module "service_role" {
  count = var.create ? 1 : 0

  source = "github.com/ministryofjustice/modernisation-platform-github-oidc-role?ref=v3.2.0"

  github_repositories = var.allowed_github_repositories
  role_name           = "${var.name_prefix}-expired-account-deleter-service-role"

  # Override the default list of attached policies
  policy_arns  = []
  policy_jsons = var.create ? [data.aws_iam_policy_document.service_role[0].json] : []

  tags = var.tags
}
