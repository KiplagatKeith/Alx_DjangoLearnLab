from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedViewSet, LikePostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"feed/", FeedViewSet, basename='feed')  
router.register(r'like', LikePostViewSet, basename='like')

urlpatterns = router.urls
