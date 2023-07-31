'''
__author__ = "Meshcomm Engineering"
__copyright__ = "Copyright (C) 2022 Meshcomm Engineering"
__version__ = '1.0'
__version__ = "20220917"

Gets message from queue in rabbitmq
'''

import pika

queue = input("Enter Unit ID: ")

 #creates connection channel
parameters = pika.URLParameters('amqps://hmuleotw:ClE61cvcxCmzKGdhsJ4oCEWibxZRvYCZ'
                                '@cold-grey-hog.rmq3.cloudamqp.com/hmuleotw')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# pylint: disable=unused-argument
def callback(chan, method, properties, body):
    """
    Gets information from queue.

    Parameters:
        body: the information stored in the queue
    """
    print(f"\nmessage: {body}")
    channel.close()



#gets the message from the queue
channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
