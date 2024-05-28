import unittest
from io import BytesIO
from unittest.mock import patch
from PIL import Image
import app  # Importing the Flask app

class TestOCRApp(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        print("\nSetting up the test environment...")

    def test_no_file_part(self):
        print("Testing absence of file part in the request...")
        response = self.app.post('/ocr')
        self.assertEqual(response.status_code, 400, "Should fail because 'file' part is missing in POST request")
        self.assertIn('No file part', response.json['error'], "Error message should indicate missing 'file' part")

    def test_empty_filename(self):
        print("Testing request with empty filename...")
        data = {'file': (BytesIO(b"dummy content"), '')}
        response = self.app.post('/ocr', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 400, "Should fail because the filename is empty")
        self.assertIn('No selected file', response.json['error'], "Error message should indicate no file was selected")

    @patch('app.easyocr')
    def test_valid_file_upload(self, mock_easyocr):
        print("Testing valid file upload...")
        mock_easyocr.return_value = {'Amount': '#100#', 'Check No': '123456'}
        img = Image.new('RGB', (60, 30), color = (73, 109, 137))
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        data = {'file': (img_byte_arr, 'test.png')}
        response = self.app.post('/ocr', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200, "Should succeed with status code 200")
        self.assertIn('ocr_result', response.json, "Response JSON should contain 'ocr_result' key")
        self.assertEqual(response.json['ocr_result'], {'Amount': '#100#', 'Check No': '123456'},
                         "OCR results should match the expected output")

    def test_valid_file_upload_with_local_image(self):
        print("Testing valid file upload with local image...")
        with patch('app.easyocr') as mock_easyocr:
            mock_easyocr.return_value = {
                "Amount": "#25,538.00#",
                "Check No": "Dooooo 125"
            }

            # Specify the path to your local image file here
            with open("./Bank Check.jpeg", "rb") as img_file:
                data = {'file': (img_file, 'Bank Check.jpeg')}
                response = self.app.post('/ocr', content_type='multipart/form-data', data=data)

            self.assertEqual(response.status_code, 200, "Should succeed with status code 200")
            self.assertIn('ocr_result', response.json, "Response JSON should contain 'ocr_result' key")
            self.assertEqual(response.json['ocr_result'], {
                "Amount": "#25,538.00#",
                "Check No": "Dooooo 125"
            }, "OCR results should match the expected output")
            
    def test_invalid_route(self):
        print("Testing an invalid route...")
        response = self.app.get('/invalid_route')
        self.assertEqual(response.status_code, 404, "Should fail with 404 because route is invalid")

if __name__ == '__main__':
    unittest.main(verbosity=2)
