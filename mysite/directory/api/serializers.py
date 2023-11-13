from django.contrib.auth import get_user_model
from rest_framework import serializers

from directory.api.fields import SameCompanySlugRelatedField

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """

    reports_to = SameCompanySlugRelatedField(
        relation_field="company",
        slug_field="pk",
        queryset=User.objects.all(),
        allow_null=True,
        required=False,
    )
    company = serializers.SlugRelatedField(slug_field="pk", read_only=True)
    reports = serializers.SerializerMethodField()
    managers = serializers.SerializerMethodField()
    num_reports = serializers.SerializerMethodField()
    is_isolated = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "pk",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "reports_to",
            "company",
            "num_reports",
            "is_isolated",
            "reports",
            "managers",
        ]
        read_only_fields = ["pk"]

    def get_reports(self, obj):
        include_reports = self.context.get("include_reports", False)
        if include_reports:
            reports_queryset = obj.reports.all()
            serializer = UserSerializer(
                reports_queryset, many=True, context={"include_reports": True}
            )
            return serializer.data

        return None

    def get_managers(self, obj):
        include_managers = self.context.get("include_managers", False)
        if include_managers and obj.reports_to:
            manager_instance = obj.reports_to
            serializer = UserSerializer(
                manager_instance, context={"include_managers": True}
            )
            return serializer.data

        return None

    def get_num_reports(self, obj):
        return User.objects.filter(reports_to=obj).count()

    def get_is_isolated(self, obj):
        return obj.reports_to is None and obj.reports.count() == 0
