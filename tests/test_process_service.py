import unittest
from unittest.mock import patch, MagicMock
from process_service import app

class TestProcessService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('process_service.s3')
    @patch('process_service.sqs')
    def test_process_message_success(self, mock_sqs, mock_s3):
        mock_file_obj = MagicMock()
        mock_file_obj.read.return_value = b'name,email\nJohn,john@example.com\nJane,jane@example.com'
        mock_s3.get_object.return_value = {'Body': mock_file_obj}

        mock_session = MagicMock()
        with patch('process_service.db_session') as mock_db_session:
            mock_db_session.return_value.__enter__.return_value = mock_session

        message = {
            'file_key': 'test.csv',
            'ReceiptHandle': 'test-receipt-handle'
        }

        process_service.process_message(message)

        mock_s3.delete_object.assert_called_once()
        mock_sqs.delete_message.assert_called_once()
        mock_session.add.assert_called()

    @patch('process_service.s3')
    @patch('process_service.sqs')
    def test_process_message_error(self, mock_sqs, mock_s3):
        mock_s3.get_object.side_effect = Exception('Error retrieving file')

        message = {
            'file_key': 'test.csv',
            'ReceiptHandle': 'test-receipt-handle'
        }

        process_service.process_message(message)

        mock_s3.delete_object.assert_not_called()
        mock_sqs.delete_message.assert_not_called()

    @patch('process_service.sqs')
    def test_main_no_messages(self, mock_sqs):
        mock_sqs.receive_message.return_value = {}

        with self.app.app_context():
            process_service.main()

        mock_sqs.receive_message.assert_called_once()

    @patch('process_service.sqs')
    @patch('process_service.process_message')
    def test_main_with_messages(self, mock_process_message, mock_sqs):
        mock_sqs.receive_message.return_value = {
            'Messages': [
                {'Body': '{"file_key": "test1.csv"}', 'ReceiptHandle': 'receipt-handle-1'},
                {'Body': '{"file_key": "test2.csv"}', 'ReceiptHandle': 'receipt-handle-2'}
            ]
        }

        with self.app.app_context():
            process_service.main()

        self.assertEqual(mock_process_message.call_count, 2)
        mock_sqs.receive_message.assert_called_once()
