from django import test
from django.urls import reverse,resolve
from ..views import *

class TestsUrls(test.SimpleTestCase):

    def test_home_page_resolved(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func.view_class, HomePageView)

    def test_signup_page_resolved(self):
        url = reverse("reg")
        self.assertEqual(resolve(url).func.view_class, RegistrationPageView,"SignUp url test")

    def test_signin_page_resolved(self):
        url = reverse("signin")
        self.assertEqual(resolve(url).func.view_class, SignInPageView,"SignIn url test")
    
    def test_history_page_resolved(self):
        url = reverse("history")
        self.assertEqual(resolve(url).func.view_class, ConvertionHistoryPageView,"History url test")

    def test_history_remove_page_resolved(self):
        url = reverse("remove", kwargs={'id':1})
        self.assertEqual(resolve(url).func.view_class, RemoveConvertionPageView,"History remove url test")
    
    def test_convertors_page_resolved(self):
        url = reverse("convertors")
        self.assertEqual(resolve(url).func.view_class, ConvertorsPageView, "Convertors url test")

    def test_csv_to_xml_page_resolved(self):
        url = reverse("csv-to-xml", kwargs={'slug':"csv-to-xml"})
        self.assertEqual(resolve(url).func.view_class, ConvertionPageView, "CSV-to-XML url test")

    def test_pdf_to_docx_page_resolved(self):
        url = reverse("pdf-to-docx", kwargs={'slug':"pdf-to-docx"})
        self.assertEqual(resolve(url).func.view_class, ConverterPdfToDocxPageView, "PDF-to-DOCX url test")
    
    def test_image_convertor_page_resolved(self):
        url = reverse("image-convertor", kwargs={'slug':"image-convertor"})
        self.assertEqual(resolve(url).func.view_class, ConvertionPngToIcoPageView,"Image Convertor url test")

    

    
    
    
     
     
        
    