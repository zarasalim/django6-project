from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import EmployeeFilter
from .models import Employee
from .permissions import EmployeePermission, MoveEmployeePermission
from .serializers import (
    EmployeeDetailSerializer,
    EmployeeSerializer,
    MoveEmployeeSerializer,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related(
        'workplace'
    ).prefetch_related('images').all()

    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter
    permission_classes = [EmployeePermission]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer

        if self.action == 'move':
            return MoveEmployeeSerializer

        return EmployeeSerializer

    @action(
        detail=True,
        methods=['patch'],
        url_path='move',
        permission_classes=[MoveEmployeePermission],
    )
    def move(self, request, pk=None):
        employee = self.get_object()

        serializer = MoveEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workplace = serializer.validated_data['workplace']

        try:
            with transaction.atomic():
                employee.workplace = workplace
                employee.save()
        except DjangoValidationError as exc:
            raise ValidationError(
                exc.message_dict if hasattr(
                    exc, 'message_dict'
                ) else exc.messages
            )

        return Response(
            EmployeeDetailSerializer(employee).data,
            status=status.HTTP_200_OK,
        )