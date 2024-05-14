from rest_framework import serializers

from inventory.models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'title', 'description')
