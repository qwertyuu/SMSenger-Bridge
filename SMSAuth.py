import re
import threading

from MessengerReceiver import MessengerReceiver
from PipelineHandler import PipelineHandler


class SMSAuth:
    def __init__(self, sms_facebook_repository, sms_listener, messenger_listen):
        self.messenger_listen = messenger_listen
        self.sms_listener = sms_listener
        self.sms_facebook_repository = sms_facebook_repository

    def receive_sms(self, message):
        from_number = message['from_number']
        text = message['text']
        if self.sms_facebook_repository.is_logged_in(from_number):
            return {
                'client': self.sms_facebook_repository.get(from_number),
                'text': text
            }

        text_search = re.search(r"^\+LOGIN ([^:]+):(.*)$", text)
        if text_search is None:
            return None
        username = text_search.group(1)
        password = text_search.group(2)
        if username is not None:
            client = MessengerReceiver(username, password)
            client.phone_number = from_number

            messenger_event_pipeline = PipelineHandler([
                self.sms_listener.send_callback
            ])
            messenger_listen_thread = threading.Thread(target=self.messenger_listen, args=[client, messenger_event_pipeline])
            messenger_listen_thread.start()
            self.sms_facebook_repository.set(from_number, client)
            print('logged in')
