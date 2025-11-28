from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile, UserSettings

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Créer le profil utilisateur à la création du compte"""
    if created:
        UserProfile.objects.get_or_create(user=instance)
        UserSettings.objects.get_or_create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarder le profil utilisateur"""
    try:
        instance.detailed_profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
