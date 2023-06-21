from django.test import TestCase
from django.conf import settings
from ..forms import ConvertionForm,ConvertionImagesForm,IMAGE_CHOICES
import os 

class TestForms(TestCase):

    def test_base_convertion_form(self):
        with open(os.path.join(settings.BASE_DIR,"csvtoxml/tests/media_test/Resume-Serhii-Kolodiazhnyi_3.pdf"),"rb") as file:
            form = ConvertionForm(
                files={
                    "file_from":file
                }
            )            
        self.assertTrue(form.is_valid())

    def test_base_convertion_invalid_form(self):
        form = ConvertionForm(data={})            
        self.assertFalse(form.is_valid())

    def test_image_convertion_form(self):
        with open(os.path.join(settings.BASE_DIR,"csvtoxml/tests/media_test/Screenshot_2.jpg"),"rb") as file:
            form = ConvertionImagesForm(
                files={
                    "file_from":file,
                },
                data={
                    "fr":IMAGE_CHOICES[1],
                    "to":IMAGE_CHOICES[0]
                }
            )            
        self.assertTrue(form.is_valid())
    
    def test_image_convertion_invalid_form(self):
        form = ConvertionImagesForm(
            data={}
        )            
        self.assertFalse(form.is_valid())

    def test_image_convertion_invalid_with_some_data_form(self):
        with open(os.path.join(settings.BASE_DIR,"csvtoxml/tests/media_test/Screenshot_2.jpg"),"rb") as file:
            form = ConvertionImagesForm(
                files={
                    "file_from":file,
                },
                data={
                    "fr":IMAGE_CHOICES[1],
                }
            )            
        self.assertFalse(form.is_valid())

    