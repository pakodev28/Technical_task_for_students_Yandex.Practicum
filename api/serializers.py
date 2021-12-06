from django.contrib.auth import get_user_model
from rest_framework import serializers

from .fields import OrgSlugRelatedField
from .models import EditingRight, Organization, Worker

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )
        write_only_fields = ("password",)
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = (
            "id",
            "full_name",
            "position",
            "work_number",
            "private_number",
            "fax",
        )


class WorkerCreateSerizalizer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(
        slug_field="id", read_only=True
    )

    class Meta:
        model = Worker
        fields = (
            "organization",
            "full_name",
            "position",
            "private_number",
            "work_number",
            "fax",
        )


class OrganizationSerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        exclude = ("creator", "editors")


class CreateDestroyEditingRightSerializer(serializers.ModelSerializer):
    editor = serializers.SlugRelatedField(
        slug_field="email", queryset=User.objects.all()
    )
    organization = OrgSlugRelatedField(slug_field="name")

    class Meta:
        model = EditingRight
        fields = ("id", "organization", "editor")


class ListEditorsSerializer(serializers.ModelSerializer):
    editor = serializers.SlugRelatedField(slug_field="email", read_only=True)
    organization = serializers.SlugRelatedField(
        slug_field="name", read_only=True
    )

    class Meta:
        model = EditingRight
        fields = (
            "editor",
            "organization",
        )
