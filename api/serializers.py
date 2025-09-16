from rest_framework import serializers
from .models import *

class PaganteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagante
        fields = '__all__'