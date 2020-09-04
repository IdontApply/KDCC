
variable "bucket" {
  description = "bucket"
}

resource "aws_s3_bucket" "a" {
  bucket = "workflowkdcc"
  acl    = "private"

  tags = {
    Name        = "workflow"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "b" {
  bucket = "dbskdcc"
  acl    = "private"

  tags = {
    Name        = "dbs"
    Environment = "Dev"
  }
}




resource "aws_s3_bucket" "c" {
  bucket = var.bucket #"maythamalherz.com"
  acl    = "public-read"
  policy = file("policy.json")
   website {
    index_document = "index.html"
    error_document = "error.html"
    routing_rules = <<EOF
[{
    "Condition": {
        "KeyPrefixEquals": "docs/"
    },
    "Redirect": {
        "ReplaceKeyPrefixWith": "documents/"
    }
}]
EOF
  }
}
