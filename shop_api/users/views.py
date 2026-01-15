from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from .serializers import (UserCreateSerializer,
                          UserAuthSerializer,
                          ConfirmationSerializer,
                          CustomTokenObtainPairSerializer)
from users.models import  CustomUser
import random
import string
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache
from users.tasks import add, send_otp_mail
from time import sleep


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class AuthorizationAPIView(CreateAPIView):
    serializer_class = UserAuthSerializer

    def post(self, request):

        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User account is not activated yet!'}
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'User credentials are wrong!'}
        )


class RegistrationAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):

        add.delay(2, 2)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        phone_number = serializer.validated_data['phone_number']
        birthdate = serializer.validated_data['birthdate']

        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                phone_number=phone_number,
                birthdate=birthdate,
                is_active=False,
                registration_source = 'local'
            )

            code = ''.join(random.choices(string.digits, k=6))
            cache.set(f'user_confirm_code:{user.id}',
                      code,
                      timeout=300
            )
            send_otp_mail.delay(email, code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'users_cod': code
            }
        )


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        code_from_user = serializer.validated_data['code']

        key = f'user_confirm_code:{user_id}'
        saved_code = cache.get(key)

        if saved_code is None:
            return Response(
                {'error': 'Confirmation code expired or invalid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if saved_code != code_from_user:
            return Response(
                {'error': 'Incorrect confirmation code'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            cache.delete(key)

            token, _ = Token.objects.get_or_create(user=user)

        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'User account successfully activated',
                'key': token.key
            }
        )