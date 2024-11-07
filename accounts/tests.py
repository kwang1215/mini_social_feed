from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from .serializers import password_regex_validator


class UserSignupTests(APITestCase):
    def setUp(self):
        # 회원가입 URL 설정
        self.signup_url = reverse("user-signup")

    def test_signup_success(self):
        # 성공적인 회원가입 테스트
        data = {
            "username": "testuser",
            "password": "testpassword123!",
            "check_password": "testpassword123!",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "email_code": 123456,  # 이메일 코드 예시 값
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "testuser")
        self.assertTrue(User.objects.filter(username="testuser").exists())


class CustomPasswordValidatorTests(TestCase):
    def setUp(self):
        self.validator = password_regex_validator

    def test_valid_password(self):
        try:
            self.validator("ValidPass123!")  
        except ValidationError:
            self.fail("유효한 비밀번호가 ValidationError를 발생시켰습니다.")

    def test_short_password(self):
        with self.assertRaises(ValidationError) as context:
            self.validator("Short1!")  
        self.assertIn(
            "비밀번호는 최소 10자 이상이어야 하며, 숫자, 문자, 특수문자 중 2가지 이상을 포함해야 하고, 연속되는 동일 문자가 3회 이상 반복되지 않아야 합니다.",
            str(context.exception)
        )

    def test_password_without_letter(self):
        with self.assertRaises(ValidationError) as context:
            self.validator("1234567890!") 
        self.assertIn("숫자, 문자, 특수문자 중 2가지 이상을 포함해야", str(context.exception))

    def test_password_without_digit(self):
        with self.assertRaises(ValidationError) as context:
            self.validator("Passwordasd!")
        self.assertIn("숫자, 문자, 특수문자 중 2가지 이상을 포함해야", str(context.exception))

    def test_password_without_special_character(self):
        with self.assertRaises(ValidationError) as context:
            self.validator("Password123")
        self.assertIn("숫자, 문자, 특수문자 중 2가지 이상을 포함해야", str(context.exception))

    def test_password_with_repeating_characters(self):
        with self.assertRaises(ValidationError) as context:
            self.validator("Passssword123!")  
        self.assertIn("연속되는 동일 문자가 3회 이상 반복되지 않아야", str(context.exception))
