from django.db import models


class NewCategory(models.Model):

    name = models.CharField(max_length=100)
