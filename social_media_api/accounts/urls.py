from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountsViewSet, RegisterViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'accounts', AccountsViewSet, basename='accounts')
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),

    path('login/', CustomAuthToken.as_view(), name='login'),

    path('profile/', AccountsViewSet.as_view({'get': 'list'}), name='profile'),
]
