
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.dal.models.enums.leaderboard_type import LeaderboardType

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Re-enter the password for confirmation."
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'receive_emails']

    def validate(self, attrs):
        password1 = attrs.get('password1', '')
        password2 = attrs.get('password2', '')

        if password1 != password2:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
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


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password_1 = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        new_password_1 = attrs.get('new_password_1')
        new_password_2 = attrs.get('new_password2')

        if new_password_1 != new_password_2:
            raise serializers.ValidationError(
                {"new_password": "New password fields didn't match."}
            )

        return attrs


class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    modules_completed = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    def get_modules_completed(self, obj):
        try:
            leaderboard_entry = obj.leaderboard_entry.filter(leaderboard__type=LeaderboardType.GLOBAL).first()
            return leaderboard_entry.modules_completed if leaderboard_entry else 0
        except Exception:
            return 0

    def get_total_score(self, obj):
        try:
            leaderboard_entry = obj.leaderboard_entry.filter(leaderboard__type=LeaderboardType.GLOBAL).first()
            return leaderboard_entry.total_score if leaderboard_entry else 0
        except Exception:
            return 0

    def get_position(self, obj):
        try:
            leaderboard_entry = obj.leaderboard_entry.filter(leaderboard__type=LeaderboardType.GLOBAL).first()
            return leaderboard_entry.position if leaderboard_entry else None
        except Exception:
            return None

    def get_is_admin(self, obj):
        return obj.is_staff or obj.is_superuser

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "experience_level",
            "receive_emails",
            "is_admin",
            "created_at",
            "updated_at",
            "modules_completed",
            "total_score",
            "position"
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
