def receive_sms(message):
    text = message['text']
    client = message['client']
    if text == '+MUTE':
        client.muted = True
    elif text == '+UNMUTE':
        client.muted = False
    else:
        return message
