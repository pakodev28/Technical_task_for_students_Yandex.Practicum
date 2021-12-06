from rest_framework.serializers import SlugRelatedField

from .models import Organization


class OrgSlugRelatedField(SlugRelatedField):
    def get_queryset(self):
        queryset = Organization.objects.all()
        request = self.context.get("request")
        if not request.user.is_superuser:
            queryset = queryset.filter(creator=request.user)
        return queryset
