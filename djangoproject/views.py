from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from django.shortcuts import get_object_or_404

"""
Login alternative: example:


@api_view(["POST"])
def login(request):
    user = authenticate(
        username=request.data["username"],
        password=request.data["password"],
    )
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"error": "Invalid credentials"},
        status=status.HTTP_401_UNAUTHORIZED,
    )


"""


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    token, created = Token.objects.get_or_create(user=user)
    return Response(
        {"token": token.key, "user": UserSerializer(user).data},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"message": "Token is valid"})
