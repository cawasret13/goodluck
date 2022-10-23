from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from db.Serializer import SerMetro, SerRegion
from db.models import Metro, Region


class MetroView(ModelViewSet):
    queryset = Metro.objects.all()
    serializer_class = SerMetro

class RegionView(ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = SerRegion
