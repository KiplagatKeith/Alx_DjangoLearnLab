from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedViewSet, LikePostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

# Don't register feed with a trailing slash in the router
feed_list = FeedViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', feed_list, name='feed'),  # <-- this creates /feed/
    path('posts/<int:pk>/like/', LikePostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:pk>/unlike/', LikePostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]
