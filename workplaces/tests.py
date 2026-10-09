from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Workplace


class WorkplaceModelTests(TestCase):
    def test_workplace_creation(self):
        workplace = Workplace.objects.create(
            desk_number=1,
            additional_information="Стол у окна",
        )

        self.assertEqual(workplace.desk_number, 1)
        self.assertEqual(
            workplace.additional_information,
            "Стол у окна",
        )

    def test_workplace_string_representation(self):
        workplace = Workplace.objects.create(
            desk_number=1,
        )

        self.assertEqual(
            str(workplace),
            "Рабочее место №1",
        )

    def test_desk_number_must_be_unique(self):
        Workplace.objects.create(desk_number=1)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Workplace.objects.create(desk_number=1)