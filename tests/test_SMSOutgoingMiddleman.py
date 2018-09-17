import unittest
from unittest.mock import MagicMock

from SMSOutgoingMiddleman import SMSOutgoingMiddleman


class TestMiddleman(unittest.TestCase):

    def test_callback_called(self):
        def sms_messenger(x): self.assertEqual(x, 'hello')
        def messenger_sms(x): self.assertEqual(x, 'hello')
        handler = SMSOutgoingMiddleman(sms_messenger, messenger_sms)
        handler.sms_to_messenger_callback('hello')
        handler.messenger_to_sms_callback('hello')

    def test_callback_toggles_sms(self):
        sms_messenger = MagicMock()
        messenger_sms = MagicMock()
        handler = SMSOutgoingMiddleman(sms_messenger, messenger_sms)

        handler.sms_to_messenger('+DISABLE')
        handler.messenger_to_sms('hello')
        handler.sms_to_messenger('+ENABLE')
        handler.messenger_to_sms('hey')

        messenger_sms.assert_called_once_with('hey')


if __name__ == '__main__':
    unittest.main()
