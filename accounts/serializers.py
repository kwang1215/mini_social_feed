from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    checkpassword = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    emailcode = serializers.IntegerField(write_only=True, required=False)

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
        if not validate_data.get("email"):
            raise serializers.ValidationError({"email": "이메일을 입력해주세요."})
        if not validate_data.get("emailcode"):
            raise serializers.ValidationError({"emailcode": "이메일코드를 입력해주세요."})

        if validate_data["password"] != validate_data["checkpassword"]:
            raise serializers.ValidationError({"non_field_errors": ["똑같은 비밀번호를 입력하세요."]})
        
        try:
            validate_password(validate_data["password"])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        
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
        # user.full_clean()  
        user.save()

        return user
