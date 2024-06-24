import os
import unittest
from Server import app  # Import the Flask app
from flask_testing import TestCase
from io import BytesIO
import pandas as pd


class AppTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_index(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_upload_file(self):
        with open('C:/Users/HHR6/PycharmProjects/TASK4-IDM/Discac_IDM_2024.xml', 'w') as f:
            f.write('<root><child>test</child></root>')

        with open('C:/Users/HHR6/PycharmProjects/TASK4-IDM/Discac_IDM_2024.xml', 'rb') as f:
            response = self.client.post('/upload', content_type='multipart/form-data',
                                        data={'file': (BytesIO(f.read()), 'C:/Users/HHR6/PycharmProjects/TASK4-IDM/Discac_IDM_2024.xml')})

        os.remove('C:/Users/HHR6/PycharmProjects/TASK4-IDM/Discac_IDM_2024.xml')

        self.assert200(response)
        self.assert_template_used('parsed.html')


    def test_new_route(self):
        response = self.client.get('/new_route')
        self.assert200(response)
        self.assert_template_used('output.html')

    """def test_download_file(self):
        # Create a sample Excel file for testing
        sample_data = {'A': [1, 2], 'B': [3, 4]}
        df = pd.DataFrame(sample_data)
        df.to_excel('output.xlsx', index=False)

        response = self.client.get('/new_routes')
        self.assert200(response)
        self.assertEqual(response.headers['Content-Disposition'], 'attachment; filename=output.xlsx')

        os.remove('output.xlsx')"""


if __name__ == '__main__':
    unittest.main()
