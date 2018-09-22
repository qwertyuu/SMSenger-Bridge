import unittest
from unittest.mock import MagicMock
from flask import Flask
from BandwidthSmsHandler import BandwidthSmsHandler


class TestBandwidthSmsHandler(unittest.TestCase):

    def setUp(self):
        self.handler = BandwidthSmsHandler('user', 'token', 'secret', 'from', 'to')

    def test_registers_in_flask(self):
        flask = Expando()
        flask.add_url_rule = MagicMock()
        self.handler.register_with_flask(flask)

        self.assertEqual('/bandwidth', flask.add_url_rule.call_args[0][0])
        self.assertTrue(callable(flask.add_url_rule.call_args[1]['view_func']))

    def test_callback_creates_sms(self):
        self.handler.bandwidth_client = Expando()
        self.handler.bandwidth_client.send_message = MagicMock()
        self.handler.send_callback('message')

        self.handler.bandwidth_client.send_message.assert_called_once_with(from_='from', text='message', to='to')

    def test_callback_is_called_if_numbers_match(self):
        callback = MagicMock()
        self.handler.start(callback)
        with Flask(__name__).test_request_context('/sms?text=hello&from=to'):
            self.handler._BandwidthSmsHandler__sms_event()

        callback.assert_called_once_with('hello')

    def test_callback_is_ignored_if_numbers_do_not_match(self):
        callback = MagicMock()
        self.handler.start(callback)
        app = Flask(__name__)
        with app.test_request_context('/sms?text=hello&from=1234'):
            self.handler._BandwidthSmsHandler__sms_event()

        callback.assert_not_called()


class Expando:
    pass


if __name__ == '__main__':
    unittest.main()
