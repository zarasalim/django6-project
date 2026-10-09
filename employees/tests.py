from django.test import TestCase
from django.urls import reverse

from .models import Employee


class EmployeeViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.employee = Employee.objects.create(
            first_name="Иван",
            last_name="Иванов",
            gender="Мужской",
            skills="Python",
    )

    def test_home_page_status_code(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    def test_employee_list_status_code(self):
        response = self.client.get(reverse("employee_list"))

        self.assertEqual(response.status_code, 200)

    def test_employee_list_context(self):
        response = self.client.get(reverse("employee_list"))

        self.assertIn("employees", response.context)
        self.assertIn(
            self.employee,
            response.context["employees"],
        )

    def test_employee_detail_status_code(self):
        response = self.client.get(
            reverse(
                "employee_detail",
                kwargs={"pk": self.employee.pk},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_employee_detail_context(self):
        response = self.client.get(
            reverse(
                "employee_detail",
                kwargs={"pk": self.employee.pk},
            )
        )

        self.assertEqual(
            response.context["employee"],
            self.employee,
        )