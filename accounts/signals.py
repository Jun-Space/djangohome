from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Subscriber


def subscriber_profile(sender, instance, created, **kwargs):
    if created:
        Subscriber.objects.create(
            user=instance,
        )


post_save.connect(subscriber_profile, sender=User)
