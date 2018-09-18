class SMSOutgoingMiddleman:
    def __init__(self):
        self.messenger_to_sms_enabled = True

    def sms_to_messenger(self, message):
        if message == '+MUTE':
            self.messenger_to_sms_enabled = False
        elif message == '+UNMUTE':
            self.messenger_to_sms_enabled = True
        else:
            return message

    def messenger_to_sms(self, message):
        return message if self.messenger_to_sms_enabled else None
