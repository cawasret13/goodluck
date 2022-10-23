from rest_framework.serializers import ModelSerializer

from db.models import Metro, Region


class SerMetro(ModelSerializer):
    class Meta:
        model = Metro
        fields = ['name']

class SerRegion(ModelSerializer):
    class Meta:
        model = Region
        fields = ['name']
