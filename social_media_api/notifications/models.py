from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Notification(models.Model):
    # The user who receives the notification
    recipient = models.ForeignKey(User, 
                                  on_delete=models.CASCADE, 
                                  related_name="notifications")
    
    # The user who triggered the notification ie liked the post
    actor = models.ForeignKey(User, 
                              on_delete=models.CASCADE, 
                              related_name="actions")
    
    # The action performed by the actor ie like, followed etc.
    verb = models.CharField(max_length=255)
    
    # Generic relation to the target object (post, comment, etc.)
    target_content_type = models.ForeignKey(ContentType, 
                                            on_delete=models.CASCADE,
                                            null=True,
                                            blank=True)
    
    # ID of the target object
    target_object_id = models.PositiveIntegerField(null=True, 
                                                   blank=True)
    
    # What action was performed on the target object
    target = GenericForeignKey('target_content_type', 
                                      'target_object_id')
    
    # When the notification was created
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Whether the notification has been read
    read = models.BooleanField(default=False)