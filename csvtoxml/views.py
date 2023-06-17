from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.views.generic import TemplateView
from allauth.account.views import SignupView,LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ConvertionForm,ConvertionImagesForm
from .models import Category,Convertion
import pandas as pd
import string
import random
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from .utils import error_checker
import uuid
import pytesseract
import os
from pdf2docx import Converter
from PIL import Image
# Create your views here.

def file_name_generator(len):
    str = ""
    for i in range(len):
        str += string.ascii_letters[random.randint(0,20)]
    return str


class HomePageView(TemplateView):
    template_name = "home/base_home.html"

class RegistrationPageView(SignupView):
    template_name = "home/reg.html"

class SignInPageView(LoginView):
    template_name = "home/login.html"

class ConvertorsPageView(LoginRequiredMixin,View):

    def get(self,request):
        categories = Category.objects.all()
        return render(request=request,template_name="csv-to-xml/home.html",context={"cats":categories,"conv":request.user.csvtoxml.all()})
    
class RemoveConvertionPageView(LoginRequiredMixin,View):
    def post(self,request,id):
        convertion = get_object_or_404(Convertion,id=uuid.UUID(id))
        try:
            convertion.delete()
            request.session['message'] = "Your convertion is successfully removed!"
            return redirect('history')
        except:
            return render(request=request,template_name="home/history.html",context={"message":"Error!"})

class ConvertionPngToIcoPageView(LoginRequiredMixin,View):
    
    def get(self,request,slug):
        cat = get_object_or_404(Category,slug=slug)
        return render(request=request,template_name="csv-to-xml/png-to-ico.html",context={"cat":cat,"form":ConvertionImagesForm()})
    
    def post(self,request,slug):
        cat = get_object_or_404(Category,slug=slug)    
        form = ConvertionImagesForm(request.POST,request.FILES)
        fr = request.POST['fr']
        to = request.POST['to']
        if fr == to:
            form.add_error('fr','Please select something another type of image!')
            form.add_error('to','Please select something another type of image!')
        error_checker(request=request,form=form,fr=fr)
        if not form.is_valid():
            return render(request=request,template_name="csv-to-xml/png-to-ico.html",context={"cat":cat,"form":form})
        name = request.FILES['file_from'].name.split(".")[0]+"."+to
        form = Convertion.objects.create(category=cat)
        form.file_from.save(request.FILES['file_from'].name,request.FILES['file_from'])
        with open(os.path.join(settings.BASE_DIR,"media/"+form.file_from.name),'rb') as file:
            form.file_to.save(name,file)
        form.save()
        request.user.csvtoxml.add(form)
        return render(request=request,template_name="home/base_home.html", context={"message":"The file was converted successfully! All your converts you can see in your history ^_^"})


class ConverterPdfToDocxPageView(LoginRequiredMixin,View):
    
    def get(self,request,slug):
        cat = get_object_or_404(Category,slug=slug)
        return render(request=request,template_name="csv-to-xml/csv-to-xml.html",context={"name":cat.name,"form":ConvertionForm()})
    
    def post(self,request,slug):
        cat = get_object_or_404(Category,slug=slug)
        form = ConvertionForm(request.POST,request.FILES)
        error_checker(request=request,form=form,fr="pdf")
        if not form.is_valid():
            return render(request=request,template_name="csv-to-xml/png-to-ico.html",context={"cat":cat,"form":form}) 
        convert = Convertion.objects.create(category=cat)
        convert.file_from.save(request.FILES['file_from'].name,request.FILES['file_from'])
        name = "media\\to\\"+convert.file_from.name.split('/')[1].split('.')[0]+"."+"docx"
        conv = Converter(os.path.join(settings.BASE_DIR,"media/"+convert.file_from.name))
        conv.convert(os.path.join(settings.BASE_DIR,name),start=0,end=None)
        conv.close()
        with open(os.path.join(settings.BASE_DIR,name),'rb') as file:
            convert.file_to.save(name.split('\\')[2],file)
        convert.save()
        request.user.csvtoxml.add(convert)
        return render(request=request,template_name="home/base_home.html", context={"message":"The file was converted successfully! All your converts you can see in your history ^_^"})
        


class ConvertionPageView(LoginRequiredMixin,View):
    form = ConvertionForm()

    def get(self,request,slug):
        cat = get_object_or_404(Category,slug=slug)
        return render(request=request,template_name="csv-to-xml/csv-to-xml.html",context={"name":cat.name,"form":ConvertionPageView.form})
    
    def post(self,request,slug):
        cat = get_object_or_404(Category,slug=slug)
        name = request.FILES['file_from'].name.split(".")[0]+".xml"
        form = ConvertionForm(request.POST,request.FILES)
        try:
            readed = pd.read_csv(request.FILES['file_from'])
        except:
            pass
        error_checker(request=request,form=form,fr="csv")
        if not form.is_valid():
            return render(request=request,template_name="csv-to-xml/csv-to-xml.html",context={"name":cat.name,"form":form})
        entireop = '<Items>\n'
        att = readed.columns
        rowop = ''
        # Going for all columns
        for j in range(len(readed)):
            rowop+="<Item>\n"
            # Going for all rows
            for i in range(len(att)):
                try:
                    tag = att[i].replace(" ","").replace("\"","").replace("'","")
                    if type(readed[att[i]][j]) == str:
                        info = readed[att[i]][j].replace(" ","").replace("\"","").replace("'","")
                    else:
                        info = readed[att[i]][j]
                    rowop+=f"<{tag}>{info}</{tag}>\n"
                except KeyError:
                    continue
            rowop+="</Item>\n"
        entireop+=rowop+"</Items>"
        # Saving in xml file all from variable (entireop)
        user = request.user
        form = Convertion.objects.create(category=cat)
        form.file_from = request.FILES['file_from']
        form.file_to.save(name,ContentFile(entireop))
        user.csvtoxml.add(form)
        form.save()

        return render(request=request,template_name="home/base_home.html", context={"message":"The file was converted successfully! All your converts you can see in your history ^_^"})

class DownloadFromPageView(LoginRequiredMixin,View):
    def get(self,request,id):
        convertion = get_object_or_404(Convertion,id=uuid.UUID(id))
        response = HttpResponse(FileWrapper(convertion.file_from))
        return response

class DowloadToPageView(LoginRequiredMixin,View):
    def get(self,request,id):
        convertion = get_object_or_404(Convertion,id=uuid.UUID(id))
        response = HttpResponse(FileWrapper(convertion.file_to))
        return response

class ConvertionHistoryPageView(LoginRequiredMixin,View):
    template_name = "home/history.html"

    def get(self,request):
        context = {}
        if 'message' in request.session:
            context = {
                "message":request.session['message']
            }
            del request.session['message']
        return render(template_name=ConvertionHistoryPageView.template_name,request=request,context=context)



