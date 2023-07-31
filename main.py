"""
__author__ = "Meshcomm Engineering"
__copyright__ = "Copyright (C) 2023 Meshcomm Engineering"
__version__ = '2.0'
__version__ = "20230220"

push_wifi_config.py
6/23/2023
Gets the wifi name and password from the user and sends them to the specified unit

functions:
    main()
    upload_firebase(wifi_name:str, cpuid:str)
    upload_rabbitmq(cpuid:str, message:str)
    delete()
"""
#Libraries
import json
import paho.mqtt.client as mqtt
import functions_framework
import pika
from google.cloud import firestore
from google.cloud.exceptions import NotFound


#setup firebase
db = firestore.Client()

# pylint: disable=locally-disabled, multiple-statements, fixme, broad-exception-caught
def upload_firebase(wifi_name:str, cpuid:str):
    """
    Checks if Unit ID exists then uploads to firebase

    Parameters: 
        cpuid(str): the Unit ID
        wifi_name(str): name of the wifi the user entered
    """

    while True:
        try:
            #adding to firebase
            db.collection('hardware').document(cpuid).update({'ssid':wifi_name})
            return True

        except NotFound:
            return ("Unit ID " + cpuid + "was not found", 404)

        except Exception as err:
            return err

        else:
            break

def upload_rabbitmq(cpuid:str, message:str):
    """
    Creates a queue in rabbitmq and uploads the message to it

    Parameters:
        cpuid(str): the Unit ID that is used to create the queue
        message(str): all the information needed to be uploaded to the unit    
    """

    #creates connection channel to rabbitmq
    parameters = pika.URLParameters('amqps://ideanomics_amqp:Y3gxIkfDq9EFtGW25DjbJ9zr55yUbiE'
                                    '@www.terralynk.com/ideanomics/?heartbeat=60'
                                    '&blocked_connection_timeout=30')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    #creating a queue in rabbitmq
    args = {"x-queue-type": "quorum"}
    args["x-message-ttl"] = 60000*5  # 300 seconds (5 minutes)
    args["x-expires"] = 360000  # 360 seconds (6 minutes)
    routing_key = f"ideanomics.solectrac.{cpuid}"
    exchange_topic = "amq.topic"
    try:

        channel.queue_declare(queue=cpuid, durable=True, arguments=args)
        channel.queue_bind(queue=cpuid, exchange=exchange_topic, routing_key=routing_key)

    except Exception as err:
        return (f"Queue failed to create {err}", 400)

    #sends the message to the specified queue
    try:

        channel.basic_publish(exchange=exchange_topic,
                            routing_key=routing_key,
                            body=message)
    except Exception as err:
        return (f"failed to publish to queue {err}", 400)

    channel.close()
    connection.close()
    return True

# pylint: disable=locally-disabled, multiple-statements, fixme, invalid-name
def MQTT(message:str):
    """
    Sends a message to a specified topic in RabbitMQ

    Parameters:
        message(str): The message to send to the topic
    """

    # Create an MQTT client instance
    client = mqtt.Client()
    client.tls_set(keyfile="config.json")
    client.username_pw_set("ideanomics:ideanomics_rem", "Ys20ir0HjoXuMCBzyX0IuRrZ8oEhP7o")

    # Connect to the MQTT broker (replace broker_address with your broker's IP/hostname)
    client.connect("www.terralynk.com", 8883, 60)

    # Start the MQTT network loop to process incoming and outgoing messages
    client.loop_start()

    client.subscribe("amq.topic")

    # Publish a message to a topic (replace test/topic with your desired topic)
    client.publish("amq.topic", message)

    client.loop_stop()


@functions_framework.http
def wifi_config(request):
    """
    Gets Unit ID, wifi name, and wifi password from user. Calls upload_firebase 
    and upload_rabbitmq.

    Parameters:
        request: The http request
    """

    #Setting up information to send
    try:
        cpuid = request.args.get('cpuid')
        wifi_name = request.args.get('ssid')
        wifi_pass = request.args.get('password')
        message = {"name": "add_wifi_network",
                    "type": "config_update",
                    "payload": {
                        "ssid": wifi_name,
                        "scan_ssid": 1,
                        "key_mgmt": "WPA-PSK NONE",
                        "psk": wifi_pass
                        }
                    }
    except KeyError as err:
        return (f"{err}: Somthing went wrong with the data", 400)

    if len(wifi_pass) < 8 or len(wifi_pass) > 64:
        return("Password length must be between 8 and 64 characters", 402)

    message_json = json.dumps(message)

    #calls functions to upload to firebase and rabbitmq
    response = upload_firebase(wifi_name, cpuid)
    if response is not True:
        return response

    queue_name = f"{cpuid}.actions"

    # MQTT(message_json)

    response2 = upload_rabbitmq(queue_name, message_json)
    if response2 is not True:
        return response2

    return message_json
