from django.shortcuts import render
# hit api & get json back
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Emp
from .serializers import EmpSerializer

# Create your views here.

class EmpList(APIView):
    # to read the data
    def get(self, request):
        emp1 = Emp.objects.all()
        serializer = EmpSerializer(emp1, many=True)
        return Response(serializer.data)

    # to post / INSERT / Create data
    def post(self, request):
        serializer = EmpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class EmpUpdate(APIView):
    # to update data
    def put(self, request, pk):
        task = Emp.objects.get(id=pk)
        serializer = EmpSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    # to delete data
    def delete(self, request, pk):
        task = Emp.objects.get(id=pk)
        task.delete()
        return Response('Item succsesfully delete!')

class EmpDeleteByName(APIView):
    # to delete data
    def delete(self, request, pk, fname):
        task = Emp.objects.get(id=pk, fname=fname)
        task.delete()
        return Response('Item succsesfully delete!')
