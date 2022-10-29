from rest_framework import serializers

from Calculations.models import FileData


class SerialFiles(serializers.ModelSerializer):
    class Meta:
        model = FileData
        files = 'file', 'id_user', 'path', 'id_session', 'data'
