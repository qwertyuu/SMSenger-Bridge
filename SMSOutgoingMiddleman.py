class SMSOutgoingMiddleman:
    def __init__(self, callback):
        self.callback = callback
        self.enable_outgoing = True

    def send_callback(self, message):
        if message == '+DISABLE':
            self.enable_outgoing = False
        elif message == '+ENABLE':
            self.enable_outgoing = True
        elif self.enable_outgoing:
            self.callback(message)
