terraform {
  backend "s3" {
    bucket = "my-terraform-state-bucket-test03"
    key    = "terraform_state/terraform.tfstate"
    region = "ap-south-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
provider "aws" {
  region = "ap-south-1"
  default_tags {
    tags = {
      "created-and-managed-by" = "terraform"
    }
  }
}


