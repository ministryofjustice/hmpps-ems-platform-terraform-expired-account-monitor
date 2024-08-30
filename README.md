# hmpps-ems-platform-terraform-expired-account-monitor
Terraform module to create a lambda function that lists users that haven't logged in within the maximum allowed time limit from a GitHub actions workflow.

## Usage

```hcl

module "expired_account_monitor" {
  source = "https://github.com/ministryofjustice/hmpps-ems-platform-hmpps-ems-platform-terraform-expired-account-monitor"
  version = "v0.1"

  allowed_github_repositories = [
    "<organisation>/<repo>:<ref>"
  ]

  tags             = local.tags
}
```
<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.63.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_function"></a> [function](#module\_function) | terraform-aws-modules/lambda/aws | 7.8.1 |
| <a name="module_service_role"></a> [service\_role](#module\_service\_role) | github.com/ministryofjustice/modernisation-platform-github-oidc-role | v3.2.0 |

## Resources

| Name | Type |
|------|------|
| [aws_iam_policy_document.function](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.service_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allowed_github_repositories"></a> [allowed\_github\_repositories](#input\_allowed\_github\_repositories) | Controls which GitHub repositories can use the role that is allowed to invoke the lambda. | `list(string)` | `[]` | no |
| <a name="input_create"></a> [create](#input\_create) | Controls whether resources should be created. | `bool` | `true` | no |
| <a name="input_create_package"></a> [create\_package](#input\_create\_package) | Controls whether Lambda package should be created. Can be used with var.create=false to ensure the function package builds during CI. | `bool` | `true` | no |
| <a name="input_name_prefix"></a> [name\_prefix](#input\_name\_prefix) | Prefix to apply to all resource names. | `string` | `""` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | A map of tags to assign to resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda"></a> [lambda](#output\_lambda) | Attributes associated with the lambda function. |
| <a name="output_service_role"></a> [service\_role](#output\_service\_role) | Attributes associated with the service role. |
<!-- END_TF_DOCS -->