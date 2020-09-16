from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def webhook(request):

    reply_msg = ""
    endsession = True

    if request.data['request']['type'] == 'LaunchRequest':
        reply_msg = "Hi, I am your home nigga"
        endsession = False
    elif request.data['request']['type'] == 'IntentRequest':
        if request.data['request']['intent']['name'] == 'turnon':
            place = request.data['request']['intent']['slots']['device']['value']
            device = request.data['request']['intent']['slots']['place']['value']
            reply_msg = "turning on, " + place + " " + device + "nigga"
            endsession = True
        elif request.data['request']['intent']['name'] == 'turnoff':
            place = request.data['request']['intent']['slots']['device']['value']
            device = request.data['request']['intent']['slots']['place']['value']
            reply_msg = "turning off, " + place + " " + device + "nigga"
            endsession = True
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