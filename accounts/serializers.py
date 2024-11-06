from django.conf import settings
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    checkpassword = serializers.CharField(write_only=True)
    emailcode = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "checkpassword",
            "first_name",
            "last_name",
            "email",
            "emailcode",
        )

    def validate(self, validate_data):
        if "email" not in validate_data or not validate_data["email"]:
            raise serializers.ValidationError("이메일을 입력해주세요.")
        if "emailcode" not in validate_data or not validate_data["emailcode"]:
            raise serializers.ValidationError("이메일코드를 입력해주세요.")
        if validate_data["password"] != validate_data["checkpassword"]:
            raise serializers.ValidationError("똑같은 비밀번호를 입력하세요.")
        return validate_data

    def create(self, validated_data):
        validated_data.pop("checkpassword")

        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user
