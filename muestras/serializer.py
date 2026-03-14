from rest_framework import serializers
from .models import Muestra

class MuestraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muestra
        fields = '__all__'