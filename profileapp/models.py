from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHICES = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Not to disclose'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') # user 모델과 OneToOne Match
    user_pk = models.AutoField(primary_key=True, unique=True) # Primary Key
    gender = models.SmallIntegerField(choices=GENDER_CHICES, default=2)
    nickname = models.CharField(max_length=20, unique=True, null=True)
    bio = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='profile/', null=True)

@receiver(post_save, sender=User) # receiver : post_save 이벤트가 발생할 때 마다 receive.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, user_pk=instance.id)

# create_user_profile, save_user_profile 를 호출해 User가 생성될 때 Profile 모델도 생성되도록 한다.

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

