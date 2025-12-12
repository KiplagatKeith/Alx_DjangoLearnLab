from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from .models import CustomUser

from .models import Accounts
from .serializers import AccountsSerializer, RegisterSerializer


# ----------------------
# Follow / Unfollow Views
# ----------------------
class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, pk):
        user = request.user
        target = get_object_or_404(self.get_queryset(), pk=pk)

        if user == target:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        user.following.add(target)
        return Response({"message": f"You are now following {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, pk):
        user = request.user
        target = get_object_or_404(self.get_queryset(), pk=pk)

        if user == target:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        user.following.remove(target)
        return Response({"message": f"You unfollowed {target.username}."}, status=status.HTTP_200_OK)

# ----------------------
# Accounts ViewSet (Profiles)
# ----------------------
class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = [AllowAny]

    # List followers for a given user
    def followers(self, request, pk=None):
        user = get_object_or_404(Accounts.objects.all(), pk=pk)
        data = [f.username for f in user.followers.all()]
        return Response({"followers": data})

    # List following for a given user
    def following(self, request, pk=None):
        user = get_object_or_404(Accounts.objects.all(), pk=pk)
        data = [f.username for f in user.following.all()]
        return Response({"following": data})


# ----------------------
# Registration View
# ----------------------
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user_id": user.id,
                "username": user.username,
                "token": token.key
            },
            status=status.HTTP_201_CREATED
        )


# ----------------------
# Login View
# ----------------------
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "username": user.username
        })
