from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import EditingRight, Organization, Worker
from .permissions import IsCreatorOrReadOnly, IsCreatorOrEditorOrReadOnly
from .serializers import (
    CreateDestroyEditingRightSerializer,
    ListEditorsSerializer,
    OrganizationSerializer,
    RegistrationSerializer,
    WorkerCreateSerizalizer,
    WorkerSerializer,
)

User = get_user_model()


class BaseCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass


class RegistrationViewSet(BaseCreateViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "workers__full_name",
        "workers__work_number",
        "workers__private_number",
        "workers__fax",
    ]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [
                IsCreatorOrReadOnly,
            ]
        return super(OrganizationViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class WorkerViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "full_name",
        "work_number",
        "private_number",
        "fax",
    ]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [
                IsCreatorOrEditorOrReadOnly,
            ]
        return super(WorkerViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "destroy"]:
            return WorkerSerializer
        return WorkerCreateSerizalizer

    def get_queryset(self):
        workers = Worker.objects.filter(
            organization=self.kwargs.get("organization_id")
        )
        return workers

    def perform_create(self, serializer):
        organization = get_object_or_404(
            Organization, pk=self.kwargs.get("organization_id")
        )
        serializer.save(organization=organization)


class EditingRightViewSet(
    mixins.ListModelMixin, mixins.DestroyModelMixin, BaseCreateViewSet
):
    queryset = EditingRight.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "destroy"]:
            return CreateDestroyEditingRightSerializer
        return ListEditorsSerializer

    @action(
        methods=["get"],
        detail=False,
    )
    def get_queryset(self):
        queryset = EditingRight.objects.filter(
            organization__creator=self.request.user
        )
        return queryset
