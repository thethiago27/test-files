import unittest
from unittest.mock import patch, MagicMock
from upload_service import app

class TestUploadService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('upload_service.s3')
    @patch('upload_service.sqs')
    def test_upload_file_success(self, mock_sqs, mock_s3):
        with self.app.test_client() as client:
            with client.put('/upload', data={'file': (open('tests/test_file.csv', 'rb'), 'test_file.csv')}, content_type='multipart/form-data') as response:
                self.assertEqual(response.status_code, 200)
                mock_s3.upload_fileobj.assert_called_once()
                mock_sqs.send_message.assert_called_once()

    @patch('upload_service.s3')
    @patch('upload_service.sqs')
    def test_upload_file_invalid_extension(self, mock_sqs, mock_s3):
        with self.app.test_client() as client:
            with client.put('/upload', data={'file': (open('tests/test_file.txt', 'rb'), 'test_file.txt')}, content_type='multipart/form-data') as response:
                self.assertEqual(response.status_code, 400)
                mock_s3.upload_fileobj.assert_not_called()
                mock_sqs.send_message.assert_not_called()

    def test_upload_file_no_file(self):
        with self.app.test_client() as client:
            response = client.put('/upload')
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
