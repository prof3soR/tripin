from django.db import models

# Create your models here.
class profile(models.Model):
    username=models.CharField(max_length=30, null=False)
    mobile=models.CharField(max_length=10)
    password=models.CharField(max_length=16)
    def __str__(self):
        return "%s" % (self.username)


class tripdetails(models.Model):
    username=models.ForeignKey(profile,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    destination=models.CharField(max_length=50)
    fromdate=models.DateField()
    duration=models.IntegerField()
    tripwith=models.CharField(max_length=20)
    interests=models.CharField(max_length=30)
    trip_itinerary=models.TextField()
    def __str__(self):
        return f" {self.name} {self.username}"

class secretspot(models.Model):
    user=models.ForeignKey(profile,on_delete=models.CASCADE)
    Spot_name=models.CharField(max_length=100)
    location=models.CharField(max_length=256)
    address=models.CharField(max_length=400)
    spot_images=models.ImageField(upload_to="static\images")
    desc=models.TextField()

class review_loaction(models.Model):
    user=models.ForeignKey(profile,on_delete=models.CASCADE)
    location_name=models.CharField(max_length=100)
    trip_img1=models.ImageField(upload_to="static\images\review_imgs")
    trip_img2=models.ImageField(upload_to="static\images\review_imgs")
    trip_img3=models.ImageField(upload_to="static\images\review_imgs")
    desc=models.TextField()
    rating=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.location_name} {self.user} review"
    

class category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to="static/images",blank=True)
    desc=models.TextField()
    def __str__(self):
        return f"{self.name}"


class destination(models.Model):
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image1=models.ImageField(upload_to="static/images", blank=True)
    image2=models.ImageField(upload_to="static/images",blank=True)
    image3=models.ImageField(upload_to="static/images",blank=True)
    image4=models.ImageField(upload_to="static/images",blank=True)
    image5=models.ImageField(upload_to="static/images",blank=True)
    desc=models.TextField()
    best_time_to_visit=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"