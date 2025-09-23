from rest_framework import serializers
from .models import *

class PaganteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagante
        fields = '__all__'

class PaganteNomeSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=255)
    