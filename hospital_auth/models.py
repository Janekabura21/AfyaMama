from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class HospitalUser(AbstractUser):
    hospital_name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.hospital_name
