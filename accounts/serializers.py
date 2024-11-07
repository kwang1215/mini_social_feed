from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

from .models import User
from django.core.validators import RegexValidator
from rest_framework import serializers

# Custom RegexValidator for password validation
password_regex_validator = RegexValidator(
    regex=r'^(?=.*[A-Za-z])(?=.*[\d])(?=.*[!@#$%^&*(),.?":{}|<>])(?!.*(.)\1\1).{10,}$',
    message="비밀번호는 최소 10자 이상이어야 하며, 숫자, 문자, 특수문자 중 2가지 이상을 포함해야 하고, 연속되는 동일 문자가 3회 이상 반복되지 않아야 합니다.",
)


class UserSerializer(serializers.ModelSerializer):
    check_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True, allow_blank=False)
    email_code = serializers.IntegerField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, validators=[password_regex_validator]
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "check_password",
            "first_name",
            "last_name",
            "email",
            "email_code",
        )

    def validate(self, data):
        # 비밀번호와 확인 비밀번호가 일치하는지 검사
        if data["password"] != data["check_password"]:
            raise serializers.ValidationError(
                {"check_password": "비밀번호가 일치하지 않습니다."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("check_password", None)
        validated_data.pop("email_code", None)
        
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
