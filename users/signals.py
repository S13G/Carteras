from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import User, Profile


# Create profile automatically for newly registered user
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = "Welcome to Carteras"
        body = "You have signed up to Carteras, we are glad you are here. Upload your skills, your projects and " \
               "make sure you connect with other developers. Happy coding "

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=[profile.email],
            reply_to=None,
            headers={'Content-Type': 'text/plain'},
        )
        email.send(fail_silently=False)


# function to update user information if profile is updated
@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# delete user account if profile is deleted
@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
