from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        # print('User Profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create userprofile if it does not exist
            UserProfile.objects.create(user=instance)
            # print('Profile did not exist, but was created')

        # print('User is updated')


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
    # print(instance.username, 'this user is being saved')
