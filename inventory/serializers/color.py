from rest_framework import serializers

from inventory.models import Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'title', 'description')
