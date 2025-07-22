from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema

from accounts.serializer.user_serializer import UpdateUserSerializer
from ..serializer import UserSerializer
from ..models import User


class CreateUserView(APIView):
    permission_classes = [AllowAny]  # 允许任何人注册用户

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer, 400: "Bad Request"},
        description="Create a new user account",
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={204: "No Content", 404: "Not Found"},
        description="Delete a user account by ID",
    )
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetUserListView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer(many=True)},
        description="Retrieve a list of all users",
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer, 404: "Not Found"},
        description="Retrieve user details by ID",
    )
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UpdateUserSerializer,
        responses={200: UpdateUserSerializer, 400: "Bad Request", 404: "Not Found"},
        description="Update user details by ID",
    )
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UpdateUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
