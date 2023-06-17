from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid 
from django.utils.text import slugify

class Category(models.Model):
    slug = models.SlugField(primary_key=True,unique=True,editable=False)
    name = models.CharField("Name",unique=True,max_length=50)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Convertion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    category = models.ForeignKey(Category,verbose_name="Category of convertion",on_delete=models.CASCADE)
    file_from = models.FileField(upload_to="from/",blank=True)
    file_to = models.FileField(upload_to="to/",blank=True)


class Newuser(AbstractUser):
    csvtoxml = models.ManyToManyField(Convertion,related_name='csvtoxml')
