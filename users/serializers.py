from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Used for listing users and showing/updating a single user."""

    name = serializers.SerializerMethodField()
    buildingName = serializers.CharField(source="building.name", read_only=True, default="")
    active = serializers.BooleanField(source="is_active")
    lastActive = serializers.DateTimeField(source="last_login", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "building",
            "buildingName",
            "active",
            "lastActive",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]

    def get_name(self, obj):
        return obj.get_full_name() or obj.username


class UserCreateSerializer(serializers.ModelSerializer):
    """Used only when inviting/creating a new user (needs a password)."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "role", "building"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
