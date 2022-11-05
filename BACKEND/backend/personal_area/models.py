from django.db import models

class PersonalData(models.Model):
    id = models.CharField(max_length=32, null=False, primary_key=True)
    name = models.CharField(max_length=256, null=False)
    lastname = models.CharField(max_length=256, null=False)

    def __str__(self):
        return f"{self.name}"
