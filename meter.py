import pika
import random
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)

count = 0
# for the purpose of the simulation, only run for the equivalent of one day

while count < 43200:
    message = str(random.randint(0, 9001))
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
    )

    print(f"Sent meter reading: {message} watts")
    time.sleep(2)
    count += 1

connection.close()
