from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)  # type: ignore
        return user

    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "refresh": str(token),
            "access": str(token.access_token),
        }

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        field = ("id", "username", "email", "password")

    def validate(self, attrs):
        user = User.objects.filter(username=attrs["username"]).first()
        if user is None or not user.check_password(attrs["password"]):
            raise serializers.ValidationError("Invalid username or password.")
        return user

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
        }
        token = RefreshToken.for_user(instance)
        data['refresh'] = str(token)
        data['access'] = str(token.access_token)
        return data
