from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import AccountsSerializer, RegisterSerializer
from .models import Accounts


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer

    # Only authenticated users can follow/unfollow, but reading profiles is allowed
    def get_permissions(self):
        if self.action in ['follow', 'unfollow', 'followers', 'following']:
            return [IsAuthenticated()]
        return [AllowAny()]

    # POST /api/accounts/<id>/follow/
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        user = request.user

        if user == user_to_follow:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.following.add(user_to_follow)
        return Response(
            {"message": f"You are now following {user_to_follow.username}."},
            status=status.HTTP_200_OK
        )

    # POST /api/accounts/<id>/unfollow/
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        user = request.user

        if user == user_to_unfollow:
            return Response(
                {"error": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.following.remove(user_to_unfollow)
        return Response(
            {"message": f"You unfollowed {user_to_unfollow.username}."},
            status=status.HTTP_200_OK
        )

    # GET /api/accounts/<id>/followers/
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        data = [f.username for f in user.followers.all()]
        return Response({"followers": data})

    # GET /api/accounts/<id>/following/
    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        data = [u.username for u in user.following.all()]
        return Response({"following": data})


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Registration must be open

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'user_id': user.id,
                'username': user.username,
                'token': token.key
            },
            status=status.HTTP_201_CREATED
        )


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]  # Login must be open

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
