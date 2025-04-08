from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class MotherAccount(models.Model):
    identification_number = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Store hashed passwords

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        
        return self.name


class MaternalProfile(models.Model):
    identification_number = models.CharField(primary_key=True, max_length=100)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    age = models.IntegerField()
    hospital = models.ForeignKey('MamaCare.HospitalUser', on_delete=models.CASCADE)
    date_registered = models.DateField(auto_now_add=True)

class ChildProfile(models.Model):
    mother = models.ForeignKey(MaternalProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    # ... any other fields

class Appointment(models.Model):
    maternal_profile = models.ForeignKey(MaternalProfile, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')])
