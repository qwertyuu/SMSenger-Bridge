from flask import request

from twilio.rest import Client as TwilioClient


class TwilioSmsHandler:
    def __init__(self, twilio_sid, twilio_auth_token, from_number, to_number):
        self.to_number = to_number
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
        if body and from_number == self.to_number:
            self.callback(body)
        return "nothing to see here"

    def send_callback(self, message_to_send):
        self.twilio_client.messages.create(body=message_to_send, from_=self.from_number, to=self.to_number)
