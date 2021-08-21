from confluent_kafka import Consumer
from django.core.mail import send_mail
import json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

c = Consumer({
    'bootstrap.servers': 'pkc-4ygn6.europe-west3.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.username': '2IZKKBHEP7IUGYM7',
    'sasl.password': 'oWucrGgTrYvNlylUnf3BuPde1gmEqYpiOdhR3pXa7HFQXg8TPjqZMwxWPC8rerl5',
    'sasl.mechanisms': 'PLAIN',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['email_topic'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

    order = json.loads(msg.value())

    send_mail(
        subject='An Order has been completed',
        message='Order #' + str(order['id']) + 'with a total of $' + str(order['admin_revenue']) + ' has been completed!',
        from_email='from@email.com',
        recipient_list=['admin@admin.com']
    )

    send_mail(
        subject='An Order has been completed',
        message='You earned $' + str(order['ambassador_revenue']) + ' from the link #' + order['code'],
        from_email='from@email.com',
        recipient_list=[order['ambassador_email']]
    )

c.close()
