from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

from coca import *
import random

@api_view(["GET", "POST"]) # /pagantes
#@permission_classes([IsAuthenticated])
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
    
@api_view(["GET", "PATCH", "DELETE"]) # /pagantes
#@permission_classes([IsAuthenticated])
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

@api_view(["GET"]) # /magu
#@permission_classes([IsAuthenticated])
def magu_list(request):
    if request.method == "GET":
        pagantes = Pagante.objects.all().order_by("ordem")
        serializer = PaganteSerializer(pagantes, many=True)
        nomes_pagantes = []
        for i in serializer.data:
            nomes_pagantes.append(i["nome"])
        nomes_pagantes.append("Conclave")
        return Response(verificar_ciclos(1, nomes_pagantes))

@api_view(["GET"])
def download_data(r):
    filename = "coquinha.xlsx"
    response = FileResponse(open(f"./exports/{filename}", "rb"))
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
    
@api_view(["GET"]) # /conclave
#@permission_classes([IsAuthenticated])
def conclave_data(request):
    pagantes = Pagante.objects.all()
    serializer = PaganteSerializer(pagantes, many=True)
    nomes_pagantes = []
    for i in serializer.data:
        nomes_pagantes.append(i["nome"])
    nomes_pagantes.append("Conclave")
    return Response(obter_dados_conclave(nomes_pagantes))


@api_view(["POST"]) # /sortear
#@permission_classes([IsAuthenticated])
def sortear_magu(request):
    if request.method == "POST":
        pagantes = list(Pagante.objects.all())
        random.shuffle(pagantes)

        with transaction.atomic():
            for p in range(len(pagantes)):
                pagantes[p].ordem = p + len(pagantes) + 1
            Pagante.objects.bulk_update(pagantes, ["ordem"])

            for i, p in enumerate(pagantes, start=1):
                p.ordem = i

            Pagante.objects.bulk_update(pagantes, ["ordem"])

        serializers = PaganteSerializer(Pagante.objects.all().order_by("ordem"), many=True)
        return Response(serializers.data)

@api_view(["GET"]) # /magu/{nome}
#@permission_classes([IsAuthenticated])
def magu_nome(request, nome):
    pagantes = Pagante.objects.all()
    serializers = PaganteSerializer(pagantes, many=True)
    nomes = []
    for i in list(serializers.data):
        nomes.append(i["nome"])
    data = obter_por_nome(nomes, nome)
    return Response(data)

@api_view(["GET"])
def download_nome(r, nome):
    filename = f"coquinha{nome}.xlsx"
    response = FileResponse(open(f"./exports/{filename}", "rb"))
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
