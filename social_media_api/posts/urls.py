from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)        # /posts/, /posts/<pk>/, plus like/unlike actions
router.register(r"comments", CommentViewSet)  # /comments/, /comments/<pk>/
router.register(r"feed", FeedViewSet, basename='feed')  # /feed/

urlpatterns = router.urls
