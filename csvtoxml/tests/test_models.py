from django import test
from django.contrib.auth import get_user_model
from ..models import Category,Convertion

class TestModels(test.TestCase):
    CONVERTION = None

    def setUp(self):
        get_user_model().objects.create_user(
            username = "admin",
            email = "admin@dfdaf.com",
            password = "admin"
        )
        cat = Category.objects.create(
            name = "FILE TO FILE"
        )
        TestModels.CONVERTION = Convertion.objects.create(
            category = cat
        )

    def test_user_model(self):
        self.assertEqual(get_user_model().objects.get(username="admin").get_username(), "admin")

    def test_category_model(self):
        self.assertEqual(Category.objects.get(slug="file-to-file").name, "FILE TO FILE")

    def test_convertion_model(self):
        self.assertEqual(Convertion.objects.get(),TestModels.CONVERTION)