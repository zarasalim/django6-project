from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Employee, EmployeeImage
from workplaces.models import Workplace


class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImage
        fields = ['id', 'image', 'order']


class EmployeeSerializer(serializers.ModelSerializer):
    images = EmployeeImageSerializer(many=True, read_only=True)
    workplace_number = serializers.IntegerField(
        source='workplace.desk_number',
        read_only=True,
    )

    class Meta:
        model = Employee
        fields = [
            'id',
            'first_name',
            'last_name',
            'hire_date',
            'gender',
            'skills',
            'workplace',
            'workplace_number',
            'images',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                exc.message_dict if hasattr(exc, 'message_dict') else exc.messages
            )

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                exc.message_dict if hasattr(exc, 'message_dict') else exc.messages
            )


class EmployeeDetailSerializer(EmployeeSerializer):
    workplace_details = serializers.SerializerMethodField()

    class Meta(EmployeeSerializer.Meta):
        fields = EmployeeSerializer.Meta.fields + ['workplace_details']

    def get_workplace_details(self, obj):
        if not obj.workplace:
            return None

        return {
            'id': obj.workplace.id,
            'desk_number': obj.workplace.desk_number,
            'additional_information': (
                obj.workplace.additional_information
            ),
        }


class MoveEmployeeSerializer(serializers.Serializer):
    workplace = serializers.PrimaryKeyRelatedField(
        queryset=Workplace.objects.all(),
    )