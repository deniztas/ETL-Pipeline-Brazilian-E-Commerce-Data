from pyspark.sql import SparkSession


def get_spark_session() -> SparkSession:
    """Get or create a spark session."""
    spark = SparkSession.builder.getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    # spark = SparkSession \
    #     .builder \
    #     .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
    #     .config("spark.hadoop.fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem") \
    #     .config("spark.hadoop.fs.s3a.awsAccessKeyId", aws_access_key_id) \
    #     .config("spark.hadoop.fs.s3a.awsSecretAccessKey", aws_secret_access_key) \
    #     .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.profile.ProfileCredentialsProvider") \
    #     .config("spark.hadoop.fs.s3a.endpoint", "us-west-2.amazonaws.com") \
    #     .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark
