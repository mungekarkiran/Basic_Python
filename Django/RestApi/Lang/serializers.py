from rest_framework import serializers
from .models import myLang

class myLangSerializer(serializers.ModelSerializer):
    class Meta:
        model = myLang
        fields = ('id','url','name','year')