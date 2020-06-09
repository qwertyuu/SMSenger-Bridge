import unittest
from unittest.mock import MagicMock

from SMSMuteControls import SMSMuteControls


class TestMiddleman(unittest.TestCase):

    def test_callback_called(self):
        def sms_messenger(x): self.assertEqual(x, 'hello')
        def messenger_sms(x): self.assertEqual(x, 'hello')
        handler = SMSMuteControls()
        self.assertEqual('hello', handler.sms_to_messenger('hello'))
        self.assertEqual('hello', handler.messenger_to_sms('hello'))

    def test_callback_toggles_sms(self):
        handler = SMSMuteControls()
        self.assertEqual(None, handler.sms_to_messenger('+MUTE'))
        self.assertEqual(None, handler.messenger_to_sms('hello'))
        self.assertEqual(None, handler.sms_to_messenger('+UNMUTE'))
        self.assertEqual('hey', handler.messenger_to_sms('hey'))


if __name__ == '__main__':
    unittest.main()
