import unittest
from unittest.mock import MagicMock
from PipelineHandler import PipelineHandler


class TestPipelineHandler(unittest.TestCase):

    def test_pipeline_stopped_when_callback_returns_falsey_data(self):
        def first(data):
            self.assertEqual('some_data', data)
            pass
        second = MagicMock()
        handler = PipelineHandler([first, second])
        handler.send_callback('some_data')
        second.assert_not_called()

    def test_pipeline_passes_modified_data_over_successfully(self):
        def first(data):
            self.assertEqual('some_data', data)
            return 'some_modified_data'
        # Note that magic mock does not return by default
        second = MagicMock()
        handler = PipelineHandler([first, second])
        handler.send_callback('some_data')
        second.assert_called_once_with('some_modified_data')

    def test_pipeline_can_call_object_method(self):
        def first(data):
            self.assertEqual('some_data', data)
            return 'some_modified_data'
        business_obj = FakeHandler()
        handler = PipelineHandler([first, business_obj.some_callback])
        handler.send_callback('some_data')

        self.assertEqual('some_modified_data', business_obj.data)


class FakeHandler:
    def __init__(self):
        self.data = None

    def some_callback(self, data):
        self.data = data


if __name__ == '__main__':
    unittest.main()
