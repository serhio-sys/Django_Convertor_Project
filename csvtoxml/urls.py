from django.urls import path
from .views import ConvertorsPageView,DownloadFromPageView,DowloadToPageView,ConverterPdfToDocxPageView,ImageReader,ConvertionPageView,ConvertionPngToIcoPageView
from .models import Category

urlpatterns = [
    path("convertors/",ConvertorsPageView.as_view(),name="convertors"),
    path("convertion/<id>/download_from/",DownloadFromPageView.as_view(),name="download_from"),
    path("convertion/<id>/download_to/",DowloadToPageView.as_view(),name="download_to"),
]

def creatingName(name):
    cat,created = Category.objects.get_or_create(name=name)
    return cat.slug

urlpatterns += [
    path("convertion/<slug>/form/csv/xml/",ConvertionPageView.as_view(),name=creatingName("CSV TO XML")),
    path("convertion/<slug>/form/pdf/docx/",ConverterPdfToDocxPageView.as_view(),name=creatingName("PDF TO DOCX")),
    path("convertion/<slug>/form/image/reader/",ImageReader.as_view(),name=creatingName("IMAGE READER")),
    path("convertion/<slug>/form/image/convertor/",ConvertionPngToIcoPageView.as_view(),name=creatingName("IMAGE CONVERTOR")),
]