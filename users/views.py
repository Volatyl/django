from .models import User
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth import login, logout

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(is_staff=False, is_superuser=False)


class CreateStaff(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_superuser=False)


class CreateSuperUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_superuser=True)


class UserLogin(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data.copy()
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
