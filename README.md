
# Generate & Aggregate

Genarate and Aggregate are Python scripts for demo and learning how to manipulate data on AWS S3 using AWSWrangler library.
Generate creates 2mln record chunks of data with transactions between random accounts and with random amounts. Based on parameters Generate prepares data for a month time for every day MLNSx2 * 2mln records. It saves data in parquet compressed format to S3 bucket. 
Aggregate takes generated data and makes sum aggregate for every day and every month for each account from data and saves aggregates to AWS S3 in csv.

## Configuration
Configure solution according to your needs and environment for execution. Following environment variables are used by scripts and can be changed by environment variables before starting container task:
REGION (eg."eu-west-1") - AWS region name where S3 bucket for data is located.
BUCKET (eg."batch-sourcedata") - AWS S3 bucket name.
MONTH (eg."202010") - month for data generation.
MLNSx2 (eg."5") - number of 2mln chunks of transaction data for generation, single chunk will have around 16,4MB.

In following installation instructions there is need to have AWS account and access it from AWS CLI.

## Installation

Build containers with Generate and Aggregate application to run them as AWS Batch task.

```bash
docker build -f genarator.Dockerfile -t generator:latest .
docker build -f aggregator.Dockerfile -t aggregator:latest .
```
Using your AWS CLI or AWS Console create registries for container images.
```bash
aws ecr create-repository --repository-name generator --image-scanning-configuration scanOnPush=true --region {REGION}
aws ecr create-repository --repository-name aggregator --image-scanning-configuration scanOnPush=true --region {REGION}
```

Authorize local Docker to your AWS ECR, to be able to push images. 
```bash
aws ecr get-login-password                                                      
docker login -u AWS -p {KEY} https://{ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/
```

Tag images for registry in your AWS account and push them.
```bash
docker tag generator:latest {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/generator:latest
docker tag aggregator:latest {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/aggregator:latest

docker push {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/generator:latest
docker push {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/aggregator:latest
```
## Running

Use published images to run in AWS Batch or any other environment for containers.
 
## License
[MIT](https://github.com/emilia-smolko/aggregate/blob/main/LICENSE)
