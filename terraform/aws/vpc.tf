# variable "profile" {
#   description = "profile"
# }
variable "region" {
  description = "region"
}
variable "shared_credentials_file" {
  description = "shared_credentials_file"
}
# Configure the AWS Provider
provider "aws" {
  version = "~> 2.0"
  region  = var.region
  profile = "default"
  shared_credentials_file = var.shared_credentials_file
}
