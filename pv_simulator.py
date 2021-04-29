import pika
import csv
import datetime


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)


def write_file(message_body):
    """
    Write a csv file in current working directory that appends with new
    values for each new message sent from the meter, as well as a timestamp,
    the value in kilowatts, and the sum of the powers (meter + PV), as requested in
    the project specifications.
    :param message body: string with the randomly generated watt amount
    :return: csv file object
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    meter_value_in_kilowatts = int(message_body) / 1000

    with open('output_file.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "meter_value", "pv_power_value", "power_sum"])
        if f.tell() == 0:  # only write header row once, at position 0
            writer.writeheader()
        writer.writerow({
                         "timestamp": timestamp,
                         "meter_value": f"{message_body} watts",
                         "pv_power_value": f"{meter_value_in_kilowatts} kilowatts",
                         "power_sum": sum([int(message_body), meter_value_in_kilowatts])
                         })


def callback(ch, method, properties, body):
    print(f"Recieved meter reading: {body.decode()} watts")
    write_file(body.decode())
    # basic_ack confirms successful delivery
    ch.basic_ack(delivery_tag=method.delivery_tag)


# basic_qos limits the unacknowledged deliveries to 1
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
