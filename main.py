import pydotenv
import threading
from flask import Flask
from facebookListenerClient import FacebookListenerClient
from twilio.rest import Client as twilioClient
from smsListener import SMSListener


def sms_to_messenger(flask_listener):
    flask_listener.run()


def messenger_to_sms(fb):
    fb.listen()


if __name__ == '__main__':
    env = pydotenv.Environment(check_file_exists=True)

    from_number = env.get('TWILIO_FROM_NUMBER')
    to_number = env.get('TWILIO_TO_NUMBER')

    flask = Flask(__name__)
    tClient = twilioClient(env.get('TWILIO_SID'), env.get('TWILIO_AUTH_TOKEN'))

    fbmessenger = FacebookListenerClient(
        env.get('MESSENGER_LOGIN'),
        env.get('MESSENGER_PASSWORD'),
        tClient,
        from_number,
        to_number
    )
    sms_listener = SMSListener(fbmessenger, tClient, from_number, to_number)
    flask.add_url_rule('/sms', view_func=sms_listener.sms_event)
    t1 = threading.Thread(target=sms_to_messenger, args=[flask])
    t2 = threading.Thread(target=messenger_to_sms, args=[fbmessenger])
    t1.start()
    t2.start()
