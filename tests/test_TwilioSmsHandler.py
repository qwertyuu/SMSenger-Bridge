import unittest
from unittest.mock import MagicMock
from flask import Flask
from TwilioSmsHandler import TwilioSmsHandler


class TestTwilioSmsHandler(unittest.TestCase):

    def setUp(self):
        self.handler = TwilioSmsHandler('sid', 'auth', 'from', 'to')

    def test_registers_in_flask(self):
        flask = Expando()
        flask.add_url_rule = MagicMock()
        self.handler.register_with_flask(flask)

        self.assertEqual('/sms', flask.add_url_rule.call_args[0][0])
        self.assertTrue(callable(flask.add_url_rule.call_args[1]['view_func']))

    def test_callback_creates_sms(self):
        self.handler.twilio_client = Expando()
        self.handler.twilio_client.messages = Expando()
        self.handler.twilio_client.messages.create = MagicMock()
        self.handler.send_callback('message')

        self.handler.twilio_client.messages.create.assert_called_once_with(body='message', from_='from', to='to')

    def test_callback_is_called_if_numbers_match(self):
        callback = MagicMock()
        self.handler.start(callback)
        with Flask(__name__).test_request_context('/sms?Body=hello&From=to'):
            self.handler._TwilioSmsHandler__sms_event()

        callback.assert_called_once_with('hello')

    def test_callback_is_ignored_if_numbers_do_not_match(self):
        callback = MagicMock()
        self.handler.start(callback)
        with Flask(__name__).test_request_context('/sms?Body=hello&From=5678'):
            self.handler._TwilioSmsHandler__sms_event()

        callback.assert_not_called()


class Expando:
    pass


if __name__ == '__main__':
    unittest.main()
