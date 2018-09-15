from fbchat import Client as fbChatClient, ThreadType


class FacebookListenerClient(fbChatClient):

    def __init__(self, email, password, twilio_client, from_number, to_number):
        super().__init__(email, password)
        self.usernames = {}
        self.twilio_client = twilio_client
        self.from_number = from_number
        self.to_number = to_number

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None,
                  thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        # If you're not the author, send
        if author_id != self.uid:
            if author_id not in self.usernames:
                user = self.fetchUserInfo(author_id)[author_id]
                self.usernames[author_id] = user.name

            self.twilio_client.messages.create(body="{}: {}".format(self.usernames[author_id], message_object.text),
                                               from_=self.from_number,
                                               to=self.to_number)
