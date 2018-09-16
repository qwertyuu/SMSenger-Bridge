from bandwidth.messaging import Client as BandwidthClient
from flask import request


class BandwidthSmsHandler:
    def __init__(self, bandwidth_user, bandwidth_token, bandwidth_secret, from_number, to_number):
        self.to_number = to_number
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
        if body and from_number == self.to_number:
            self.callback(body)
        return "nothing to see here"

    def send_callback(self, message_to_send):
        self.bandwidth_client.send_message(text=message_to_send, from_=self.from_number, to=self.to_number)
