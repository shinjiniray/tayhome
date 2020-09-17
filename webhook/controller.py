from rest_framework.decorators import api_view
from rest_framework.response import Response

from webhook.mqtthandler import publish


@api_view(['GET', 'POST'])
def webhook(request):

    reply_msg = ""
    endsession = True

    if request.data['request']['type'] == 'LaunchRequest':
        reply_msg = "Hi, I am your home nigga"
        endsession = False
    elif request.data['request']['type'] == 'IntentRequest':
        if request.data['request']['intent']['name'] == 'turnon':
            place = request.data['request']['intent']['slots']['place']['value']
            device = request.data['request']['intent']['slots']['device']['value']

            if place == "bedroom":
                topic = "device"
            else:
                topic = "device"

            if device == "light":
                pin = 0
            else:
                pin = 1

            status = publish(topic, pin, place, device, 0)
            print(status)
            if status:
                reply_msg = "Turning on, " + place + " " + device + " nigga"
                endsession = True
            else:
                reply_msg = "Couldn't turn on " + place + " " + device + " nigga"
                endsession = False
        elif request.data['request']['intent']['name'] == 'turnoff':
            place = request.data['request']['intent']['slots']['place']['value']
            device = request.data['request']['intent']['slots']['device']['value']

            if place == "bedroom":
                topic = "device"
            else:
                topic = "device"

            if device == "light":
                pin = 0
            else:
                pin = 1

            status = publish(topic, pin, place, device, 1)
            print(status)
            if status:
                reply_msg = "Turning off, " + place + " " + device + " nigga"
                endsession = True
            else:
                reply_msg = "Couldn't turn off " + place + " " + device + " nigga"
                endsession = False
        elif request.data['request']['intent']['name'] == 'AMAZON.StopIntent':
            endsession = True

    response_body = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reply_msg
            },
            "card": {
                "type": "Simple",
                "title": "Lima Chat",
                "content": reply_msg
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Please give me further information"
                }
            },
            "shouldEndSession": endsession
        }
    }

    return Response(response_body)