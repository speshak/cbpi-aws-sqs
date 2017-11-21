# CraftBeerPi to AWS SQS

## Introduction
This plugin allows CraftBeerPi 3.0 to send sensor data to an Amazon Web Services SQS queue.

## Use
1. Install boto3 (`pip install boto3`)
2. Install the plugin
3. Under Parameters add your AWS API key ID & secret, and SQS queue URL.
4. Restart CraftBeerPi


## Why?
I created this to allow me to easily get data from CraftBeerPi into AWS for
further processing.  Once the sensor messages are in SQS you can implement
Lambda functions to do any sort of post-processing you might desire.

Ideas:
* Monitor for out of range values and send alerts via SNS
* Write values to CloudWatch for monitoring.
* Track data in DynamoDB and display on a public dashboard.
