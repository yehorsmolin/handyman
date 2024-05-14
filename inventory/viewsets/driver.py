from rest_framework import viewsets
from Handyman.permissions import IsAdminUser
from inventory.models import Status
from inventory.serializers import StatusSerializer
from rest_framework.permissions import IsAuthenticated


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
