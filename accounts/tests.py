from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from django.core.exceptions import ValidationError
from accounts.validators import CustomPasswordValidator
from django.test import TestCase

class UserSignupTests(APITestCase):
    def setUp(self):
        # 회원가입 URL 설정
        self.signup_url = reverse("user-signup")

    def test_signup_success(self):
        # 성공적인 회원가입 테스트
        data = {
            "username": "testuser",
            "password": "testpassword123!",
            "checkpassword": "testpassword123!",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "emailcode": 123456,  # 이메일 코드 예시 값
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "success")
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_signup_password_mismatch(self):
        # 비밀번호가 일치하지 않을 때
        data = {
            "username": "testuser",
            "password": "testpassword123",
            "checkpassword": "differentpassword",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "emailcode": 123456,
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "똑같은 비밀번호를 입력하세요.", response.data["non_field_errors"]
        )

    # 이메일 코드 누락 테스트
    def test_signup_missing_emailcode(self):
        data = {
            "username": "testuser",
            "password": "testpassword123",
            "checkpassword": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            # emailcode 누락
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("이메일코드를 입력해주세요.", response.data.get("emailcode", []))
        


class CustomPasswordValidatorTests(TestCase):
    def setUp(self):
        self.validator = CustomPasswordValidator()

    def test_valid_password(self):
        # 유효한 비밀번호가 통과하는지 확인
        try:
            self.validator.validate("ValidPass123!")
        except ValidationError:
            self.fail("유효한 비밀번호가 ValidationError를 발생시켰습니다.")

    def test_short_password(self):
        # 너무 짧은 비밀번호가 ValidationError를 발생시키는지 확인
        with self.assertRaises(ValidationError) as context:
            self.validator.validate("Short1!")
        self.assertIn("비밀번호는 10자리 이상이어야 합니다.", str(context.exception))

    def test_password_without_letter(self):
        # 영문이 포함되지 않은 비밀번호가 ValidationError를 발생시키는지 확인
        with self.assertRaises(ValidationError) as context:
            self.validator.validate("1234567890!")
        self.assertIn(
            "비밀번호는 하나 이상의 영문이 포함되어야 합니다.", str(context.exception)
        )

    def test_password_without_digit(self):
        # 숫자가 포함되지 않은 비밀번호가 ValidationError를 발생시키는지 확인
        with self.assertRaises(ValidationError) as context:
            self.validator.validate("Passwordasd!")
        self.assertIn(
            "비밀번호는 하나 이상의 숫자가 포함되어야 합니다.", str(context.exception)
        )

    def test_password_without_special_character(self):
        # 특수문자가 포함되지 않은 비밀번호가 ValidationError를 발생시키는지 확인
        with self.assertRaises(ValidationError) as context:
            self.validator.validate("Password123")
        self.assertIn(
            "비밀번호는 적어도 하나 이상의 특수문자(!@#$%^&())가 포함되어야 합니다.",
            str(context.exception),
        )
