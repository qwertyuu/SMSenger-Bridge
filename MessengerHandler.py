from fbchat import Client as fbChatClient, ThreadType, Message
import re

from fuzzywuzzy import process


class MessengerHandler(fbChatClient):

    def __init__(self, email, password):
        super().__init__(email, password)
        self.usernames = {}
        self.recipient = None
        self.callback = None

    def start(self, callback):
        self.callback = callback
        self.listen(True)

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None,
                  thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):

        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        # If you're not the author, send
        if author_id != self.uid:
            if author_id not in self.usernames:
                self.usernames[author_id] = self.fetchThreadInfo(thread_id)[thread_id].name
            self.callback("{}: {}".format(self.usernames[author_id], message_object.text))

    def send_callback(self, message_to_send):
        text_search = re.search(r"(?:^@([^:]+)\:\s?)?(.*)", message_to_send)
        user_search_term = text_search.group(1)
        text_to_send = text_search.group(2)

        if user_search_term is not None:
            # TODO: Add memory to call the fetchAllUsers endpoint less often
            users = {user.uid: user.name for user in self.fetchAllUsers()}
            search_result = process.extractOne(user_search_term, users)
            user_id = search_result[2]
            if user_id:
                self.recipient = user_id
        self.send(Message(text=text_to_send), thread_id=self.recipient)
