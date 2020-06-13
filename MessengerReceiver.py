from fbchat import Client as fbChatClient, ThreadType, _graphql, User


class MessengerReceiver(fbChatClient):
    phone_number = None

    def __init__(self, email, password):
        super().__init__(email, password)
        self.usernames = {}
        self.muted = False
        self.recipient = None
        self.callback = None

    def searchForContacts(self, name, limit=10):
        """
        queries	"{\"o0\":{\"doc_id\":\"2268911786543136\",\"query_params\":{\"query\":\"samuel\",\"num_users\":10,\"num_groups\":8,\"num_pages\":5}}}"
        """
        """Find and get users by their name.

        Args:
            name: Name of the user
            limit: The max. amount of users to fetch

        Returns:
            list: :class:`User` objects, ordered by relevance

        Raises:
            FBchatException: If request failed
        """
        params = {"query": name, "num_users": limit, 'num_groups': 8, 'num_pages': 5}
        (j,) = self.graphql_requests(_graphql.from_doc_id('2268911786543136', params))

        return [User._from_graphql(node['node']) for node in j['messenger_search']['result_modules']['nodes'][0]['search_results']['edges']]

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
