from rest_framework import viewsets, permissions, filters, status, generics
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]

    # Enables searching posts by title or content
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)

        # Create notification for the post author
        if comment.post.author != self.request.user:
            post_ct = ContentType.objects.get_for_model(Post)
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented",
                target_content_type=post_ct,
                target_object_id=comment.post.id
            )
            
class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        # Get posts from users the current user follows
        return Post.objects.filter(author__in=following_users).order_by('-created_at') 
    

class LikePostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # POST /posts/<post_id>/like/
    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        # Get post or return 404
        post = generics.get_object_or_404(Post, pk=pk)

        # Prevent duplicate likes
        like, created = Like.objects.get_or_create(user=request.user, post=post)  # checker wants request.user
        if not created:
            return Response({"error": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification if liking someone else's post
        if post.author != request.user:
            post_ct = ContentType.objects.get_for_model(Post)
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked",
                target_content_type=post_ct,
                target_object_id=post.id
            )

        return Response({"success": "Post liked"}, status=status.HTTP_201_CREATED)

    # POST /posts/<post_id>/unlike/
    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike(self, request, pk=None):
        # Get post or return 404
        post = generics.get_object_or_404(Post, pk=pk)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
        except Like.DoesNotExist:
            return Response({"error": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the notification if it exists
        Notification.objects.filter(
            recipient=post.author,
            actor=request.user,
            verb="liked",
            target_object_id=post.id
        ).delete()

        return Response({"success": "Post unliked"}, status=status.HTTP_200_OK)
