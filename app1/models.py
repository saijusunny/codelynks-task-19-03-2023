
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", 'Staff'
        USERS = "USERS", 'Users'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)
    image=models.ImageField(upload_to="image/", null=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class StaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STAFF)


class Staff(User):

    base_role = User.Role.STAFF

    users=StaffManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Staff"

@receiver(post_save, sender=Staff)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STAFF":
        StaffProfile.objects.create(user=instance)


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.IntegerField(null=True, blank=True)

class UsersManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.USERS)


class Users(User):

    base_role = User.Role.USERS

    users=UsersManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Users"

@receiver(post_save, sender=Users)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "USERS":
        UsersProfile.objects.create(user=instance)


class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    users_id = models.IntegerField(null=True, blank=True)



class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description=models.TextField()
    tag = models.CharField(max_length=50, null=True)
    like = models.IntegerField(null=True,default=0)
    dislike = models.IntegerField(null=True,default=0)

class files(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(post, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='images/upload/', null=True, blank=True)

class liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(post, on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=50, null=True)

class disliked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(post, on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=50, null=True)

    


