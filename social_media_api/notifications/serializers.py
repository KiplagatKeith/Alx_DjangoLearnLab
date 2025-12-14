from rest_framework import serializers
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_str = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor_username', 'verb', 'target_str', 'timestamp', 'read']

    def get_target_str(self, obj):
        if obj.target:
            return str(obj.target)  # This calls the __str__ method of the target object
        return None
