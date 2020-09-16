import json
import threading
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT


class MQTTHandler(threading.Thread):

    def __init__(self):
        pass

    def run(self):
        args = {
            'client_id': 'abcdefghijkl',
            'endpoint': 'a8jyxx32q2p0a-ats.iot.ap-south-1.amazonaws.com',
            'cert': '/home/pi/src/certs/cert pem/232ef22a93-certificate.pem.crt',
            'key': '/home/pi/src/certs/private key/232ef22a93-private.pem.key',
            'root_ca': '/home/pi/src/certs/rootCA.pem'
        }

        # Create an AWS IoT MQTT Client using TLSv3.1 Mutual Authentication
        self.myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(args['client_id'], protocolType=AWSIoTPyMQTT.MQTTv3_1)
        self.myAWSIoTMQTTClient.configureEndpoint(args['endpoint'], 443)
        self.myAWSIoTMQTTClient.configureCredentials(args['root_ca'], args['key'], args['cert'])
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 128, 20)
        print('Connecting...')
        if self.myAWSIoTMQTTClient.connect(1200):
            print('Connected')
            while True:
                pass
        else:
            print('Not Connected')

    def publish(self, pin, what):
        return self.myAWSIoTMQTTClient.publish("device", json.dumps({"device_pin":pin, "what":what}), 0)


t = None


def publish(place, device, what):
    global t
    pin = 0
    return t.publish(pin, what)


def initialize():
    global t
    t = MQTTHandler()
    t.start()
