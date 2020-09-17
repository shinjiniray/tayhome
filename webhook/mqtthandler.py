import json
import threading
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT


class MQTTHandler(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        args = {
            'client_id': 'jgvnrevnrew',
            'endpoint': 'a8jyxx32q2p0a-ats.iot.ap-south-1.amazonaws.com',
            'cert': '/home/ec2-user/tayhome/certs/mqtt/certpem/232ef22a93-certificate.pem.crt',
            'key': '/home/ec2-user/tayhome/certs/mqtt/privatekey/232ef22a93-private.pem.key',
            'root_ca': '/home/ec2-user/tayhome/certs/mqtt/rootCA.pem'
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

    def publish(self, topic, pin, what):
        return self.myAWSIoTMQTTClient.publish(topic, json.dumps({"device_pin":pin, "what":what}), 0)


t = MQTTHandler()


def publish(topic, pin, place, device, what):
    global t
    return t.publish(topic, pin, what)


def initialize():
    global t
    t = MQTTHandler()
    t.start()

