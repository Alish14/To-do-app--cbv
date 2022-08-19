from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, ChangePasswordSerializer, ProfileSerializers, ActivationResendSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from ...models import User
from ..utils import EmailThread
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError,InvalidSignatureError


class RegistrationView(generics.GenericAPIView):
    serializer_class=RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer =RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]

            data={
                # 'username':serializer.validated_data['username'],
                "email": email


            }
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.GenericAPIView):
     
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializers
    queryset=User.objects.all()
    def get_object(self):
        queryset=self.get_queryset()
        obj = get_object_or_404(queryset, username=self.request.user)
        if  not obj.is_verify:
            raise Response(
                {'detail': 'user not validate'})

        return obj

class EmailSendView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        message = EmailMessage('email/hello.tpl',{'name': 'alish'}, 'admin@admin.com',to=['alish14.mod@gmail.com'])
        message.send()
        return Response("email Sent")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj=User.objects.get(pk=user_id)
        user_obj.is_verified=True
        user_obj.save()
        return Response({"detail":"your account has been verified"})


class ActivationResendView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer
    def post(self, request,*args, **kwargs):
        serializer=ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "user activation resend successfully"},
            status=status.HTTP_200_OK,
        )
    def get_tokens_for_user(self, user):
            refresh = RefreshToken.for_user(user)
            return str(refresh.access_token)

