import paho.mqtt.client as paho
from paho import mqtt
# import mqtt_callbacks as callbacks
from paho.mqtt.client import connack_string

class MQTT:

    def __init__(self, client_id : str = "User0", broker : str = "e94ecb09544d4cd39ee5231c33b0f001.s2.eu.hivemq.cloud", port : int = 8883, keepalive : int = 60):
        self.client = paho.Client(client_id=client_id)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.broker = broker
        self.port = port
        self.keepalive = keepalive

    def __on_connect(self, client, userdata, flags, rc):
        print("Connected to client %s with result code %s" % (client._client_id, connack_string(rc)))

    def __on_disconnect(self, client, userdata, rc):
        print("Disconnected from client %s with result code %s" % (client._client_id, connack_string(rc)))

    def __on_message(self, client, userdata, message):
        print("Received message %s from client %s" % (message.payload, client._client_id))
        command = message.payload.decode("utf-8")
        if (command == "Go"):
            print("Đã nhận Go")

    def __on_publish(self, client, userdata, mid):
        print("Published message to client %s with message id %s" % (client._client_id, mid))

    def __on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed to client %s with message id %s and QoS %s" % (client._client_id, mid, granted_qos))

    def set_on_connect_callback(self, on_connect = None):
        if (on_connect == None):
            self.client.on_connect = self.__on_connect
        else:
            self.client.on_connect = on_connect

    def set_on_disconnect_callback(self, on_disconnect = None):
        if (on_disconnect == None):
            self.client.on_disconnect = self.__on_disconnect
        else:
            self.client.on_disconnect = on_disconnect

    def set_on_message_callback(self, on_message = None):
        if (on_message == None):
            self.client.on_message = self.__on_message
        else:
            self.client.on_message = on_message

    def set_on_publish_callback(self, on_publish = None):
        if (on_publish == None):
            self.client.on_publish = self.__on_publish
        else:    
            self.client.on_publish = on_publish   

    def set_on_subscribe_callback(self, on_subscribe = None):
        if (on_subscribe == None):
            self.client.on_subscribe = self.__on_subscribe
        else:
            self.client.on_subscribe = on_subscribe      

    def set_credentials(self, username : str, password : str):
        self.client.username_pw_set(username, password)

    def connect(self):
        self.client.connect(self.broker, port=self.port, keepalive=self.keepalive)

    def loop_start(self):
        self.client.loop_start()

    def loop_forever(self):
        self.client.loop_forever()

    def set_callback(self, on_connect: bool = False, on_disconnect: bool = False, on_message: bool = False, on_publish: bool = False, on_subscribe: bool = False):
        
        if (on_connect):
            self.set_on_connect_callback()
        if (on_disconnect):
            self.set_on_disconnect_callback()
        if (on_message):
            self.set_on_message_callback()
        if (on_publish):
            self.set_on_publish_callback()
        if (on_subscribe):
            self.set_on_subscribe_callback()

    def publish(self, topic, payload, qos = 1):
        self.client.publish(topic, payload, qos)

    def subscribe(self, topic, qos = 1):
        self.client.subscribe(topic, qos)