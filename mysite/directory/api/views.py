from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from directory.api.filtersets import UsersFilterSet
from directory.api.serializers import UserSerializer
from directory.models import User


class UsersViewSet(viewsets.ModelViewSet):
    """
    Endpoint for returning User data.
    """

    filterset_class = UsersFilterSet
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def reports(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        users = user.reports.all()
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"include_reports": True}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            users, many=True, context={"include_reports": True}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def managers(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        users = managers = [user.reports_to] if user.reports_to else []

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"include_managers": True}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            users, many=True, context={"include_managers": True}
        )
        return Response(serializer.data)

    def get_queryset(self):
        request_user = self.request.user

        return User.objects.filter(company=request_user.company)
