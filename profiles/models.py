from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    Stores default delivery info and order history for each user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country *', null=True, blank=True)
    default_postcode = models.CharField(max_length=10, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=70, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=70, null=True, blank=True)
    default_county = models.CharField(max_length=60, null=True, blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create or update a user's profile when the User object is saved.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()