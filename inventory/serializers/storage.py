from rest_framework import serializers

from inventory.models.storage import Storage


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('id', 'title', 'description')
