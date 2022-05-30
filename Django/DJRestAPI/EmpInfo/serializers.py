from rest_framework import serializers
from .models import Emp

class EmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emp
        fields = ('id','fname','lname','age','experience','salary')
        # OR
        # fields = '__all__'