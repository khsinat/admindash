from django.test import TestCase
import io
from PIL import Image

# Create your tests here.
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

# class AnalysisAPITestCase(self):
#     def test_create_analysis(self):
#         # Prepare your test data
#         url = reverse('analysis-create')  # The URL pattern name for your view
#         image = SimpleUploadedFile("/home/tanishkbox/clgproject/cannabis.jpg", b"file_content", content_type="image/jpeg")
#         data = {
#             'number_of_plants': 3,
#             'branches_per_plant': 5,
#             'desired_goals': 'Increase yield',
#             'cannabis_files':[image]
#         }
#         client= self.APIClient()
#         response= client.post(url, data, format='multipart')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Prepare files to upload
        # with open('/home/tanishkbox/clgproject/cannabis.jpg', 'rb') as img1:
        #     files = {
        #         'cannabis_files': [img1]
        #     }
        #     response = self.client.post(url, data, format='multipart', files=files)
        # print(response.data)
        # Assert the response status
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert the response data (this will depend on your actual response structure)
#         "number_of_plants": 5,
#         "branches_per_plant": 4,
#         "desired_goals": "High yield",
#         "cannabis_files": [open('path_to_image.jpg', 'rb')]  # Use an actual image or mock image data
#     }
#     response = self.client.post(url, data, format='multipart')
#     print(response.data)  # This will show the detailed error message
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
class AnalysisTests(APITestCase):
    def test_create_analysis(self):
        url = reverse('analysis-create')  # Replace with your correct URL name for the analysis list

        # Create an image in memory using Pillow
        image = Image.new('RGB', (100, 100), color='red')  # Create a red image (100x100)
        img_io = io.BytesIO()  # Create a bytes buffer
        image.save(img_io, 'JPEG')  # Save the image in JPEG format to the buffer
        img_io.seek(0)  # Rewind the buffer to the beginning

        # Use the in-memory image as the file
        image_file = SimpleUploadedFile("/home/tanishkbox/clgproject/cannabis.jpg", img_io.read(), content_type="image/jpeg")

        # Prepare the data for the API request
        data = {
            "number_of_plants": 5,
            "branches_per_plant": 4,
            "desired_goals": "High yield",
            "cannabis_files": [image_file]  # Ensure 'cannabis_files' is sent as a list
        }

        # Create the API client and send the request
        client = APIClient()
        response = client.post(url, data, format='multipart')  # Ensure format is 'multipart'

        # Check the response
        print(response.data)  # Debug: print the response to check errors
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Assert that the status code is 201

