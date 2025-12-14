from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedViewSet, LikePostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"feed", FeedViewSet, basename='feed')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:pk>/like/', LikePostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:pk>/unlike/', LikePostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]
