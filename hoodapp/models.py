from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime as dt

# Create your models here.
class Neighborhood(models.Model):
    name = models.CharField(max_length = 30)
    user_id = models.ForeignKey(User,blank=True, on_delete=models.CASCADE,related_name='user',null=True)
    location = models.CharField(max_length = 30)

    def save_category(self):
        self.save()

    def delete_category(self):
        self.delete()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length = 30)
    profile_pic = models.ImageField(upload_to='profile/')
    pub_date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.first_name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class Business(models.Model):
    business_name = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 30)
    neighbourhood = models.ForeignKey(Neighborhood, blank=True, null=True)


# @classmethod
# def search_by_name(cls,search_term):
#     business = cls.neighbourhood = models.ForeignKey(neighbourhood, related_name='businesses')objects.filter(title__icontains=search_term)
#     return business

class Post(models.Model):
    user = models.ForeignKey(Profile, related_name='profile')
    post = models.CharField(max_length=30)
    neighborhood = models.ForeignKey(Neighborhood, related_name='posts')           

