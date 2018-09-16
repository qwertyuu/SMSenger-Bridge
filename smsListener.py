from fbchat import Message
from flask import request
import re


class SMSListener:
    def __init__(self, messenger, to_number):
        self.messenger = messenger
        self.recipient = None
        self.to_number = to_number

    def sms_event(self):
        body = request.args.get('Body')
        from_number = request.args.get('From')
        if body and from_number == self.to_number:
            text_search = re.search(r"(?:^@([^:]+)\:\s?)?(.*)", body)
            if text_search.group(1) is not None:
                search_result = self.messenger.searchForUsers(text_search.group(1))
                if len(search_result):
                    first_result = search_result[0]
                    self.recipient = first_result.uid
            text_to_send = text_search.group(2)
            if self.recipient and text_to_send:
                self.messenger.send(Message(text=text_to_send), thread_id=self.recipient)
        return "nothing to see here"
