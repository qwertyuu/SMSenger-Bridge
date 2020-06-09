import threading
from flask import Flask
from BandwidthSmsHandler import BandwidthSmsHandler
from MessengerDispatch import MessengerDispatch
import SMSMuteControls
from SMSAuth import SMSAuth
from SMSFacebookRepository import SMSFacebookRepository
from TwilioSmsHandler import TwilioSmsHandler
from PipelineHandler import PipelineHandler
import os
from dotenv import load_dotenv


def get_sms_provider(provider_name):
    if provider_name == 'bandwidth':
        return BandwidthSmsHandler(
            os.getenv('BANDWIDTH_USER'),
            os.getenv('BANDWIDTH_TOKEN'),
            os.getenv('BANDWIDTH_SECRET'),
            os.getenv('BANDWIDTH_FROM_NUMBER'),
        )
    elif provider_name == 'twilio':
        return TwilioSmsHandler(
            os.getenv('TWILIO_SID'),
            os.getenv('TWILIO_AUTH_TOKEN'),
            os.getenv('TWILIO_FROM_NUMBER'),
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
    load_dotenv()

    flask = Flask(__name__)
    sms_listener = get_sms_provider(os.getenv('SMS_PROVIDER'))

    auth = SMSAuth(SMSFacebookRepository(), sms_listener, messenger_listen)

    sms_event_pipeline = PipelineHandler([
        auth.receive_sms,
        SMSMuteControls.receive_sms,
        MessengerDispatch().send_message
    ])

    sms_listen_thread = threading.Thread(target=sms_listen, args=[
        flask,
        sms_listener,
        sms_event_pipeline,
        os.getenv('FLASK_HOST', None),
        os.getenv('FLASK_PORT', '5000')
    ])
    sms_listen_thread.start()
