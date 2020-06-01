import pydotenv
import threading
from getpass import getpass
from flask import Flask

from BandwidthSmsHandler import BandwidthSmsHandler
from MessengerHandler import MessengerHandler
from SMSOutgoingMiddleman import SMSOutgoingMiddleman
from TwilioSmsHandler import TwilioSmsHandler
from PipelineHandler import PipelineHandler


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


def sms_listen(flask_listener, sms_handler, pipeline, host, port):
    sms_handler.register_with_flask(flask)
    sms_handler.start(pipeline.send_callback)
    flask_listener.run(host=host, port=port, debug=False)


def messenger_listen(fb, pipeline):
    fb.start(pipeline.send_callback)


if __name__ == '__main__':
    env = pydotenv.Environment(check_file_exists=True)

    flask = Flask(__name__)

    fbmessenger = MessengerHandler(
        env.get('MESSENGER_LOGIN'),
        env.get('MESSENGER_PASSWORD')
    )
    sms_listener = get_sms_provider(env.get('SMS_PROVIDER'), env)
    middleman = SMSOutgoingMiddleman()

    sms_event_pipeline = PipelineHandler([
        middleman.sms_to_messenger,
        fbmessenger.send_callback
    ])
    messenger_event_pipeline = PipelineHandler([
        middleman.messenger_to_sms,
        sms_listener.send_callback
    ])

    sms_listen_thread = threading.Thread(target=sms_listen, args=[
        flask,
        sms_listener,
        sms_event_pipeline,
        env.get('FLASK_HOST', None),
        env.get('FLASK_PORT', '5000')
    ])
    messenger_listen_thread = threading.Thread(target=messenger_listen, args=[fbmessenger, messenger_event_pipeline])
    sms_listen_thread.start()
    messenger_listen_thread.start()
