import os
from bandwidth.messaging import Client as BandwidthClient
from flask import request
from twilio.request_validator import RequestValidator


class BandwidthSmsHandler:
    def __init__(self, bandwidth_user, bandwidth_token, bandwidth_secret, from_number):
        self.from_number = from_number
        self.bandwidth_client = BandwidthClient(bandwidth_user, bandwidth_token, bandwidth_secret)
        self.callback = None

    def register_with_flask(self, flask):
        flask.add_url_rule('/bandwidth', view_func=self.__sms_event)

    def start(self, callback):
        self.callback = callback

    def __sms_event(self):
        body = request.args.get('text')
        from_number = request.args.get('from')
        validator = RequestValidator(os.getenv('TWILIO_AUTH_TOKEN'))

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        if request_valid and body:
            self.callback({
                'from_number': from_number,
                'text': body,
            })
        return "nothing to see here"

    def send_callback(self, message_to_send):
        self.bandwidth_client.send_message(
            text=message_to_send['text'],
            from_=self.from_number,
            to=message_to_send['client'].phone_number,
        )
