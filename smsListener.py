from fbchat import Message
from flask import request
from fuzzywuzzy import process
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
            user_search_term = text_search.group(1)
            text_to_send = text_search.group(2)

            if user_search_term is not None:
                users = {user.uid: user.name for user in self.messenger.fetchAllUsers()}
                search_result = process.extractOne(user_search_term, users)
                user_id = search_result[2]
                if user_id:
                    self.recipient = user_id

            if self.recipient and text_to_send:
                self.messenger.send(Message(text=text_to_send), thread_id=self.recipient)
        return "nothing to see here"
