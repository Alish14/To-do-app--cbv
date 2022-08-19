from xml.dom import ValidationErr
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from ...models import Profile,User


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password1']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError(
                {'detail': 'passwords does not match'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1',None)
        return User.objects.create_user(**validated_data)
class ChangePasswordSerializer(serializers.Serializer):
    model=User
    old_password=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True)
    new_password1=serializers.CharField(required=True)
    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password1'):
            raise serializers.ValidationError(
                {'detail': 'passwords does not match'})
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)})

        return super().validate(attrs)
class ProfileSerializers(serializers.ModelSerializer):
    email=serializers.CharField(source="user.email",read_only=True)

    class Meta:
        model=Profile
        fields = ("id",
                  "email",
                  "first_name",
                  "last_name",
                  "image",
                  "description",)
        read_only_fields=('email',)
class ActivationResendSerializer(serializers.Serializer):
    email=serializers.EmailField(require=True)

    def validate(self, attrs):
        email=attrs.get("email")
        try:
            user_obj=User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail':'cant find user with this email !'})
        # if user_obj.verified:
        #     raise serializers.ValidationError({'detail':'user is already verified'})
        attrs['user']=user_obj
        return super().validate(attrs)
 
