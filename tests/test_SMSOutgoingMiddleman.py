import unittest
from unittest.mock import MagicMock

from SMSOutgoingMiddleman import SMSOutgoingMiddleman


class TestMiddleman(unittest.TestCase):

    def test_callback_called(self):
        def callback(x): self.assertEqual(x, 'hello')
        handler = SMSOutgoingMiddleman(callback)
        handler.send_callback('hello')

    def test_callback_toggles_outbound(self):
        callback = MagicMock()
        handler = SMSOutgoingMiddleman(callback)

        handler.send_callback('+DISABLE')
        handler.send_callback('+ENABLE')
        handler.send_callback('hello')
        handler.send_callback('+DISABLE')
        handler.send_callback('bye')

        callback.assert_called_once_with('hello')


if __name__ == '__main__':
    unittest.main()
