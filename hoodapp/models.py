from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime as dt
from tinymce.models import HTMLField

# Create your models here.
class Neighbourhood(models.Model):
    name = models.CharField(max_length = 30)
    user_id = models.ForeignKey(User,blank=True, on_delete=models.CASCADE,related_name='user',null=True)
    location = models.CharField(max_length = 30)
    image = models.ImageField(upload_to='neighimage/', null=True)
    # admin = models  admin = models.ForeignKey(Profile, related_name='hoods', null=True).ForeignKey(Profiles,related_name='hoods', null=True)
    def save_category(self):
        self.save()

    def delete_category(self):
        self.delete()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    email = models.EmailField(max_length = 30)
    pub_date_created = models.DateTimeField(auto_now_add=True, null=True)
    neighbourhood = models.ForeignKey('Neighbourhood', blank=True, null=True)
     
    # def __str__(self):
    #     return self.first_name

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
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='businesses')
    profile = models.ForeignKey(Profile, related_name='profiles')


     
    @classmethod
    def search_by_name(cls,search_term):
        business = cls.objects.filter(title__icontains=search_term)
        return business

class Post(models.Model):
    user = models.ForeignKey(Profile, related_name='profile')
    post = models.CharField(max_length=30)
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='posts')

class Activities(models.Model):
    name = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey(User,blank=True, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey('Neighbourhood', blank=True, null=True)
    email = models.EmailField(max_length=70,blank=True)
    path = models.ImageField(upload_to = 'gallery/')    



