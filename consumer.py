import django
import json
import os
import pika
import logging

logging.basicConfig()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

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

channel.queue_declare(queue='admin')
# channel.exchange_declare(exchange="test_exchange",
#                          exchange_type="direct",
#                          passive=False,
#                          durable=True,
#                          auto_delete=False)


def callback(ch, method, properties, body):
    print('Received in admin')
    product_id = json.loads(body)
    print(product_id)
    product = Product.objects.get(id=product_id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased')


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
