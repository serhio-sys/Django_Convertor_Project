from django import forms

IMAGE_CHOICES = (
        ("png","png"),
        ("jpg","jpg"),
        ("ico","ico"),
        ("webp","webp"),
    )

class ConvertionForm(forms.Form):
    file_from = forms.FileField(required=True)

class ConvertionImagesForm(forms.Form):
    fr = forms.ChoiceField(choices=IMAGE_CHOICES,required=True,label="From")
    to = forms.ChoiceField(choices=IMAGE_CHOICES,required=True)
    file_from = forms.FileField(required=True)