class SMSFacebookRepository:
    number_to_client = {}

    def is_logged_in(self, number):
        return number in self.number_to_client

    def get(self, number):
        return self.number_to_client.get(number)

    def set(self, number, client):
        self.number_to_client[number] = client
