output "lambda" {
  description = "Attributes associated with the lambda function."
  value       = module.function
}

output "service_role" {
  description = "Attributes associated with the service role."
  value = module.service_role
}
