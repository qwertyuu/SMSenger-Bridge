from fbchat import Client as fbChatClient, ThreadType


class MessengerReceiver(fbChatClient):
    phone_number = None

    def __init__(self, email, password):
        super().__init__(email, password)
        self.usernames = {}
        self.muted = False
        self.recipient = None
        self.callback = None

    def start(self, callback):
        self.callback = callback
        self.listen(True)

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None,
                  thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        if self.muted:
            return

        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        # If you're not the author, send
        if author_id != self.uid:
            if author_id not in self.usernames:
                self.usernames[author_id] = self.fetchThreadInfo(thread_id)[thread_id].name
            self.callback({
                'text': "{}: {}".format(self.usernames[author_id], message_object.text),
                'client': self
            })
