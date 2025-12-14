from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        # Unread first, then by newest
        return Notification.objects.filter(recipient=user).order_by('read', '-timestamp')

    # Custom action to mark as read
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        notification.read = True
        notification.save()
        return Response({"success": "Notification marked as read"}, status=status.HTTP_200_OK)
