from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
