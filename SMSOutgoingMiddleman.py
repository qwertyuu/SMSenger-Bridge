class SMSOutgoingMiddleman:
    def __init__(self, sms_to_messenger_callback, messenger_to_sms_callback):
        self.sms_to_messenger_callback = sms_to_messenger_callback
        self.messenger_to_sms_callback = messenger_to_sms_callback
        self.sms_to_messenger_enabled = True
        self.messenger_to_sms_enabled = True

    def sms_to_messenger(self, message):
        if message == '+MUTE':
            self.messenger_to_sms_enabled = False
        elif message == '+UNMUTE':
            self.messenger_to_sms_enabled = True
        else:
            self.sms_to_messenger_callback(message)

    def messenger_to_sms(self, message):
        if self.messenger_to_sms_enabled:
            self.messenger_to_sms_callback(message)
