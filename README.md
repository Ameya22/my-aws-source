# my-aws-stuff

It uses Amazon S3, Amazon Simple Notification Service(SNS) & AWS Lambda

boto3 is Python SDK for AWS

Before executing lambda function, follow below steps on AWS console:
1) Create bucket in Amazon S3 & upload config.json file in this bucket
2) Create SNS topic & add subscriptions as per your choice
3) Create a Lambda function to get random name from list, read S3 object(config.json), update output of lambda function into S3 object and publish the output to SNS topic
4) Test lambda function by creating Test event

Change bucket permissions: uncheck below 2 points under Block all public access:
	Block public access to buckets and objects granted through new access control lists (ACLs)
  Block public access to buckets and objects granted through any access control lists (ACLs)

Add Bucket policy:
	{
	    "Version": "2012-10-17",
	    "Statement": [
	        {
	            "Effect": "Allow",
	            "Principal": "*",
	            "Action": [
	                "s3:PutObject",
	                "s3:PutObjectAcl",
	                "s3:GetObject",
	                "s3:GetObjectAcl",
	                "s3:DeleteObject"
	            ],
	            "Resource": [
	                "arn:aws:s3:::<your-bucket-name>",
	                "arn:aws:s3:::<your-bucket-name>/*"
	            ]
	        }
	    ]
}

