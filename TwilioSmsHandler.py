import os
from flask import request
from twilio.request_validator import RequestValidator

from twilio.rest import Client as TwilioClient


class TwilioSmsHandler:
    def __init__(self, twilio_sid, twilio_auth_token, from_number):
        self.from_number = from_number
        self.twilio_client = TwilioClient(twilio_sid, twilio_auth_token)
        self.callback = None

    def register_with_flask(self, flask):
        flask.add_url_rule('/sms', view_func=self.__sms_event)

    def start(self, callback):
        self.callback = callback

    def __sms_event(self):
        body = request.args.get('Body')
        from_number = request.args.get('From')
        validator = RequestValidator(os.getenv('TWILIO_AUTH_TOKEN'))

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        """
        request_valid = validator.validate(
            request.url,
            request.args,
            request.headers.get('X-TWILIO-SIGNATURE', ''))
        """

        if request.headers.get('User-Agent') == 'TwilioProxy/1.1' and body:
            self.callback({
                'from_number': from_number,
                'text': body,
            })
        return "nothing to see here"

    def send_callback(self, message_to_send):
        self.twilio_client.messages.create(
            body=message_to_send['text'],
            from_=self.from_number,
            to=message_to_send['client'].phone_number,
        )
