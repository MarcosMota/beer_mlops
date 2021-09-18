resource "aws_kinesis_stream" "kinesis_stream" {
  name             = "${var.project_name}-stream"
  shard_count      = 1
  retention_period = 24
  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]
}

resource "aws_kinesis_firehose_delivery_stream" "extended_s3_stream_transform" {
  name        = "${var.project_name}-firehouse-transform"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn   = var.role.firehouse_arn
    bucket_arn = var.bucket_transform_arn
    buffer_size     = 64
    buffer_interval = 60

    processing_configuration {
      enabled = "true"

      processors {
        type = "Lambda"

        parameters {
          parameter_name  = "LambdaArn"
          parameter_value = "${aws_lambda_function.lambda_transform.arn}:$LATEST"
        }
      }
    }

    data_format_conversion_configuration {
      input_format_configuration {
        deserializer {
          open_x_json_ser_de {}
        }
      }

      output_format_configuration {
        serializer {
          parquet_ser_de {}
        }
      }

      schema_configuration {
        database_name = aws_glue_catalog_database.aws_glue_catalog_database.name
        role_arn      = var.role.firehouse_arn
        table_name    = aws_glue_catalog_table.aws_glue_catalog_table.name
        region        = var.region
      }
    }
  }

  kinesis_source_configuration {
    role_arn = var.role.firehouse_arn
    kinesis_stream_arn = aws_kinesis_stream.kinesis_stream.arn
  }
}


resource "aws_kinesis_firehose_delivery_stream" "extended_s3_stream_raw" {
  name        = "${var.project_name}-firehouse-extraction"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn        = var.role.firehouse_arn
    bucket_arn      = var.bucket_extraction_arn
    buffer_size     = 1
    buffer_interval = 60
  }

  kinesis_source_configuration {
    role_arn = var.role.firehouse_arn
    kinesis_stream_arn = aws_kinesis_stream.kinesis_stream.arn
  }

}
