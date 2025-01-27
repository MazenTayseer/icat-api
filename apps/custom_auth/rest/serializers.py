from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import re

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Re-enter the password for confirmation."
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def validate(self, attrs):
        email = attrs.get('email', '').strip()
        first_name = attrs.get('first_name', '').strip()
        last_name = attrs.get('last_name', '').strip()
        password1 = attrs.get('password1', '')
        password2 = attrs.get('password2', '')

        if not email or not first_name or not last_name:
            raise serializers.ValidationError(
                {"fields": "First name, last name, and email cannot be empty."}
            )

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise serializers.ValidationError(
                {"email": "Invalid email format."}
            )

        if password1 != password2:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        # Validate password strength
        if not re.search(r'[A-Z]', password1):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one uppercase letter."}
            )
        if not re.search(r'[a-z]', password1):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one lowercase letter."}
            )
        if not re.search(r'[0-9]', password1):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one digit."}
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one special character."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = User.objects.create_user(password=password, **validated_data)
        return user



class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        attrs['user'] = user
        return attrs
