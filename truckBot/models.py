from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    zoom_exe_path = models.CharField(max_length=300, blank=True)
    zoom_phone_numb = models.CharField(max_length=150, blank=True)
    landstar_firstname = models.CharField(max_length=50)
    landstar_lastname = models.CharField(max_length=50)
    landstar_credentials_path = models.CharField(max_length=250, blank=True)
    posting_allowed = models.BooleanField(default=True)
    banned = models.BooleanField(default=False)
    
    # Versions of messages that will be created
    def load_offer_str(self):
        return "[[LOAD OFFER!!]][[LOAD OFFER!!]]\n"

    def landstar_info1(self):
        return f"\n{self.landstar_firstname} Contact: {self.zoom_phone_numb}"
    
    def landstar_info2(self):
        return f"\n{self.landstar_firstname} {self.zoom_phone_numb}"

# Load from the lane found on Naviersphere. This LaneLoad will be posted on Landstar 
class LaneLoad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lane_loads")
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    pickup = models.CharField(max_length=30)
    delivery = models.CharField(max_length=30)
    miles = models.IntegerField()
    weight = models.IntegerField()
    equipment = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    posted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.origin} -> {self.destination} | Rate: ${self.price}"
    
    class Meta:
        unique_together = ('origin', 'destination', 'pickup', 'delivery', 'miles', 'weight')    
    
    
# Load info which is already existing on Landstar 
class Load(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loads")
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
        return f"{self.id}: {self.origin} -> {self.destination}"

    def save(self, *args, **kwargs):
        # If there is no message created (object is created for the first time)
        if not self.message:
            # it will have this message
            self.message = (
                f"Pick: {self.origin} -- {self.pickup}\n" +
                f"Delivery: {self.destination} -- {self.delivery}\n" +
                f"Mode: {self.mode}\n" +
                f"Miles: {self.miles}\n" +
                f"Est. Weight: {self.weight} lb\n" +
                f"RATE {self.price}")

        super().save(*args, **kwargs)


# Truck driver from the Landstar
class Driver(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=14)
    sms_sent = models.BooleanField(default=False)
    load = models.ForeignKey(Load, on_delete=models.CASCADE, related_name="drivers")
    
    def __str__(self):
        return f"{self.name} {self.phone_number} {self.sms_sent} {self.load.id}"
    
    
# Drivers informed about load posted on Landstar, through the Zoom
class LoadHistory(models.Model):
    load_id = models.IntegerField(db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loads_history")
    date = models.DateTimeField(editable=False)
    drivers_informed_count = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.localtime(timezone.now())
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.load_id} -> {self.drivers_informed_count} informed"
    
    def formatted_date(self):
        return self.date.strftime("%d.%m.%Y %H:%M")
