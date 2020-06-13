from fbchat import Message
import re
from fuzzywuzzy import process


class MessengerDispatch:
    def send_message(self, message_to_send):
        client = message_to_send['client']
        text = message_to_send['text']
        text_search = re.search(r"(?:^@([^:]+)\:\s?)?(.*)", text)
        user_search_term = text_search.group(1)
        text_to_send = text_search.group(2)

        if user_search_term is not None:
            # TODO: Add memory to call the fetchAllUsers endpoint less often
            contacts = client.searchForContacts(user_search_term)
            if len(contacts):
                client.recipient = contacts[0].uid
        client.send(Message(text=text_to_send), thread_id=client.recipient)
