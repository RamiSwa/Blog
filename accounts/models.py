from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

def default_profile_picture():
    return 'default_profile.png'  # This should point to your default profile image in your static/media directory

class CustomUser(AbstractUser):
    USER_ROLES = [
        ('admin', _('Admin')),
        ('author', _('Author')),
        ('reader', _('Reader')),
    ]

    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='reader',
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        default=default_profile_picture
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.profile_picture.path)

    def is_admin(self):
        return self.role == 'admin'

    def is_author(self):
        return self.role == 'author'
