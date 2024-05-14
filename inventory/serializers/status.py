from rest_framework import serializers

from inventory.models.status import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'title', 'description')
