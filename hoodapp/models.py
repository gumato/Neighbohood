from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime as dt
from tinymce.models import HTMLField
from pyuploadcare.dj.models import ImageField

# Create your models here.
class Neighbourhood(models.Model):
    name = models.CharField(max_length = 30)
    location = models.CharField(max_length =10)
    user_id = models.ForeignKey(User,blank=True, on_delete=models.CASCADE,related_name='user',null=True)
    image = models.ImageField(upload_to='hoodimage/', null=True)
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    occupants = models.ForeignKey(User, null = True,related_name='business')

    def save_neighbourhood(self):
        self.save()

    def delete_neigbourhood(self):
        self.delete()

    @classmethod
    def find_neighbourhood_id(cls, id):
        neighbourhood = Neighbourhood.objects.get(pk=id)
        return neighbourhood

    @classmethod
    def get_profile_neighbourhood(cls, profile):
        neighbourhood = Neighbourhood.objects.filter(profile__pk = profile)
        return neighbourhood
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    bio = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile/')
    email = models.EmailField(max_length = 30)
    neighbourhood = models.ForeignKey('Neighbourhood', blank=True, null=True)
     

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
    name = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 30)
    image = models.ImageField(upload_to='bsimage/')
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='businesses')
    profile = models.ForeignKey(Profile, related_name='profiles')

    def save_business(self):
        self.save()

     
    @classmethod
    def search_by_name(cls,search_term):
        business = cls.objects.filter(title__icontains=search_term)
        return business

class Post(models.Model):
    user = models.ForeignKey(Profile, related_name='profile')
    post = models.CharField(max_length=30)
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='posts')
 
class Location(models.Model):
    name = models.CharField(max_length=30)

    def save_location(self):
        self.save()

    def delete_location(self):
        self.delete()

    def __str__(self):
        return self.name 



