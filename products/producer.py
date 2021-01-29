import json
import pika
import logging
logging.basicConfig()

# parameters = pika.URLParameters('amqps://ikdwqznl:7LI_pxEatDH0BDfcPNPiINrXiqYRyOZ1@orangutan.rmq.cloudamqp.com
# /ikdwqznl')
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(
    host='172.18.0.22',
    port=5672,
    socket_timeout=300,
    credentials=credentials,
    heartbeat=600,
    blocked_connection_timeout=300
)

connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
