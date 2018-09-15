from fbchat import Message
from flask import request
import re


class SMSListener:
    def __init__(self, messenger, twilio, from_number, to_number):
        self.messenger = messenger
        self.twilio = twilio
        self.from_number = from_number
        self.to_number = to_number
        self.recipient = None

    def sms_event(self):
        # Add a message
        body = request.args.get('Body')
        if body:
            text_search = re.search(r"(?:@([^:]+)\:\s)?(.*)", body)
            if text_search.group(1) is not None:
                search_result = self.messenger.searchForUsers(text_search.group(1))
                if len(search_result):
                    first_result = search_result[0]
                    self.recipient = first_result.uid
                    self.twilio.messages.create(body="Switched to: {}".format(first_result.name),
                                                from_=self.from_number,
                                                to=self.to_number)
            text_to_send = text_search.group(2)
            if self.recipient and text_to_send:
                self.messenger.send(Message(text=text_to_send), thread_id=self.recipient)
        return "nothing to see here"
