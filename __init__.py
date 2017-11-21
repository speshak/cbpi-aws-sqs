from modules import cbpi
from thread import start_new_thread
import logging
import json, time
import boto3


DEBUG = False
sqs_client = None
sqs_url = None


def init_sqs_client():
    aws_access_key_id = cbpi.get_config_parameter("aws_access_key_id", None)
    aws_secret_access_key = cbpi.get_config_parameter("aws_secret_access_key", None)

    if aws_access_key_id is None:
        try:
            cbpi.add_config_parameter("aws_access_key_id", "", "text", "AWS Access Key ID")
        except:
            cbpi.notify("SQS Error", "Unable to update config parameter", type="danger")

    if aws_secret_access_key is None:
        try:
            cbpi.add_config_parameter("aws_secret_access_key", "", "text", "AWS Secret Access Key")
        except:
            cbpi.notify("SQS Error", "Unable to update config parameter", type="danger")

    global sqs_url
    sqs_url = cbpi.get_config_parameter("sqs_url", None)
    if sqs_url is None:
        try:
            cbpi.add_config_parameter("sqs_url", "", "text", "SQS Queue URL")
        except:
            cbpi.notify("SQS Error", "Unable to update config parameter", type="danger")


    cbpi.app.logger.info("Using AWS Key ID " + aws_access_key_id)
    cbpi.app.logger.info("Sending sensor data to SQS queue " + sqs_url)

    global sqs_client
    sqs_client = boto3.client(
        'sqs',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=cbpi.get_config_parameter("aws_region", "us-east-1")
    )


def send_data(data):
    resp = sqs_client.send_message(
        QueueUrl=sqs_url,
        MessageBody=json.dumps(data)
    )
    cbpi.app.logger.debug("Sent SQS message " + resp['MessageId'])


@cbpi.initalizer(order=200)
def init(cbpi):
    cbpi.app.logger.info("AWS SQS plugin initialize")
    init_sqs_client()


@cbpi.backgroundtask(key="sqs_task", interval=60)
def sqs_background_task(api):
    for key, value in cbpi.cache.get("sensors").iteritems():
        if value.hide == 1:
            continue

        data = value.instance.get_value()
        data['timestamp'] = time.time()
        data['sensor_id'] = value.instance.id
        data['sensor_name'] = value.name
        data['sensor_type'] = value.type

        send_data(data)
