from rest_framework import serializers
from .models import Ecuacion

class EcuacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ecuacion
        fields = ('id', 'imagen','ecuacion','solucion')