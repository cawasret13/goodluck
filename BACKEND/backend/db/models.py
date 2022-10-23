from django.db import models


class Metro(models.Model):
    name = models.TextField()


class Region(models.Model):
    name = models.TextField()
