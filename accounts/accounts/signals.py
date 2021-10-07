from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import File

@receiver(post_save, sender=File)
def check_file_ext(sender, instance, created, **kwargs):
    if created:
        extension_list = instance.file.name.split('.')
        extension = extension_list[1]
        instance.file_ext = extension
        instance.save()
