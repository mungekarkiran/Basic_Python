from django.shortcuts import render
from rest_framework import viewsets
from .models import myLang
from .serializers import myLangSerializer
# Create your views here.

class myLangView(viewsets.ModelViewSet):
    queryset = myLang.objects.all()
    serializer_class = myLangSerializer

# def myLangList(request):

