from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

from coca import *
import random

@api_view(["GET", "POST"])
def pagante_list(request):
    if request.method == "GET":
        pagantes = Pagante.objects.all()
        serializer = PaganteSerializer(pagantes, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PaganteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET", "PATCH", "DELETE"])
def pagante_detail(request, pk):
    pagante = get_object_or_404(Pagante, pk=pk)

    if request.method == "GET":
        serializer = PaganteSerializer(pagante)
        return Response(serializer.data)
    elif request.method == "PATCH":
        serializer = PaganteSerializer(pagante, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        pagante.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET"])
def magu_list(request):
    if request.method == "GET":
        pagantes = Pagante.objects.all()
        serializer = PaganteSerializer(pagantes, many=True)
        nomes_pagantes = []
        for i in serializer.data:
            nomes_pagantes.append(i["nome"])
        nomes_pagantes.append("Conclave")
        verificar_ciclos(4, nomes_pagantes)

        filename = "coquinha.xlsx"
        response = FileResponse(open(f"exports/{filename}", "rb"))
        response["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

@api_view(["POST"])
def sortear_magu(request):
    if request.method == "POST":
        pagantes = list(Pagante.objects.all())
        nums = []
        for i in range(len(pagantes)):
            nums.append(i + 1)
        for i in pagantes:
            num = random.choice(nums)
            nums.remove(num)
            i.id = num
            i.save()
        pagantes_novo = Pagante.objects.all()
        serializers = PaganteSerializer(pagantes_novo)
        return Response(serializers.data)

