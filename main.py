import pydotenv
import threading
from flask import Flask

from BandwidthSmsHandler import BandwidthSmsHandler
from MessengerHandler import MessengerHandler
from SMSOutgoingMiddleman import SMSOutgoingMiddleman
from TwilioSmsHandler import TwilioSmsHandler

outgoing_sms_toggle = True


def get_sms_provider(provider_name, environment):
    to_number = environment.get('YOUR_NUMBER')
    if provider_name == 'bandwidth':
        return BandwidthSmsHandler(
            environment.get('BANDWIDTH_USER'),
            environment.get('BANDWIDTH_TOKEN'),
            environment.get('BANDWIDTH_SECRET'),
            environment.get('BANDWIDTH_FROM_NUMBER'),
            to_number
        )
    elif provider_name == 'twilio':
        return TwilioSmsHandler(
            environment.get('TWILIO_SID'),
            environment.get('TWILIO_AUTH_TOKEN'),
            environment.get('TWILIO_FROM_NUMBER'),
            to_number
        )
    else:
        raise ValueError('Bad SMS_PROVIDER in .env. Choices are: [bandwidth, twilio]')


def sms_to_messenger(flask_listener, sms_handler, fb, host, port):
    sms_handler.register_with_flask(flask)
    sms_handler.start(fb.send_callback)
    flask_listener.run(host=host, port=port, debug=False)


def messenger_to_sms(fb, sms_handler):
    fb.start(sms_handler.send_callback)


if __name__ == '__main__':
    env = pydotenv.Environment(check_file_exists=True)

    flask = Flask(__name__)

    fbmessenger = MessengerHandler(
        env.get('MESSENGER_LOGIN'),
        env.get('MESSENGER_PASSWORD')
    )
    sms_listener = get_sms_provider(env.get('SMS_PROVIDER'), env)
    middleman = SMSOutgoingMiddleman(sms_listener.send_callback)
    sms_to_messenger_thread = threading.Thread(target=sms_to_messenger, args=[
        flask,
        sms_listener,
        middleman,
        env.get('FLASK_HOST', None),
        env.get('FLASK_PORT', '5000')
    ])
    messenger_to_sms_thread = threading.Thread(target=messenger_to_sms, args=[fbmessenger, sms_listener])
    sms_to_messenger_thread.start()
    messenger_to_sms_thread.start()
