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
            device = request.data['request']['intent']['slots']['device']['value']
            place = request.data['request']['intent']['slots']['place']['value']
            status = publish(place, device, 0)
            if status:
                reply_msg = "Turning on, " + place + " " + device + " nigga"
                endsession = True
            else:
                reply_msg = "Couldn't turn on " + place + " " + device + " nigga"
                endsession = False
        elif request.data['request']['intent']['name'] == 'turnoff':
            device = request.data['request']['intent']['slots']['device']['value']
            place = request.data['request']['intent']['slots']['place']['value']
            status = publish(place, device, 1)
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