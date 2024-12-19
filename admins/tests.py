from django.test import TestCase

# Create your tests here.
#测试import接口
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ImportTestCase(TestCase):
    def test_import_student(self):
        url = reverse('import_student')
        print(url)
        csv_file = open(r"C:\Users\Tirsenna\Downloads\students_info_20241209_232922(2).csv", 'rb')
        response = self.client.post(url, {'csv_file': csv_file})


        print(response.data)

    def test_import_teacher(self):
        url = reverse('import_teacher')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_import_admin(self):
        url = reverse('import_admin')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
