# AWS Organisation List Accounts

This is uses Lambda to generate a csv list with the AWS accounts under the AWS Organization. And copies the csv to an S3 bucket and generates as AWS Glue table

## Deploy

Note: require [Serverless Framework](https://www.serverless.com/framework/docs/getting-started/) installed

```
sls deploy \
--region us-east-1 \
--stage prod \
--aws-profile root
```

```
sls remove \
--region us-east-1 \
--stage prod \
--aws-profile root
```