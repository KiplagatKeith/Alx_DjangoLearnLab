from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

class Accounts(AbstractUser):
    bio = models.TextField(blank=True, 
                           null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', 
                                        blank=True,
                                        null=True)
    followers = models.ManyToManyField('self',
                                       symmetrical=False,
                                       related_name='following', 
                                       blank=True)
    
    # override groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )