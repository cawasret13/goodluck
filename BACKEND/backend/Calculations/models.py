from django.db import models
class FileData(models.Model):
    id_session = models.CharField(null=True, max_length=32)
    id_user = models.CharField(max_length=30, null=True)
    file = models.FileField(upload_to='files', null=False)
    path = models.CharField(max_length=512, null=True)
    data = models.TextField(null=True)
    id_reference = models.IntegerField(null=True)

class NumStreet(models.Model):
    id_street = models.IntegerField()
    name_street = models.TextField()