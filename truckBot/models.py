from django.db import models
from django.contrib.auth.models import AbstractUser
from cryptography.fernet import Fernet


class User(AbstractUser):
    zoom_exe_path = models.CharField(max_length=300, blank=True)
    zoom_phone_numb = models.CharField(max_length=150, blank=True)
    landstar_firstname = models.CharField(max_length=50)
    landstar_lastname = models.CharField(max_length=50)
    landstar_credentials_path = models.CharField(max_length=250, blank=True)

    def landstar_info(self):
        return f"{self.landstar_firstname} Contact: {self.zoom_phone_numb}"


class Load(models.Model):
    id = models.IntegerField(primary_key=True)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    pickup = models.CharField(max_length=30)
    delivery = models.CharField(max_length=30)
    mode = models.CharField(max_length=30)
    miles = models.IntegerField()
    weight = models.IntegerField()
    price = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"id={self.id}, {self.origin}->{self.destination}"

    def save(self, *args, **kwargs):
        if not self.message:  # This checks if the object is being created for the first time
            self.message = (
                f"[[LOAD OFFER!!]][[LOAD OFFER!!]]\n" +
                f"Pick: {self.origin} -- {self.pickup}\n" +
                f"Delivery: {self.destination} -- {self.delivery}\n" +
                f"Mode: {self.mode}\n" +
                f"Miles: {self.miles}\n" +
                f"Est. Weight: {self.weight} lb\n" +
                f"RATE {self.price}\n")

        super().save(*args, **kwargs)


class Driver(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=14)
    sms_sent = models.BooleanField(default=False)
    load = models.ForeignKey(Load, on_delete=models.CASCADE)


class LogHistory(models.Model):
    load_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)



