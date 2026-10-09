from django.db import models


class Workplace(models.Model):
    desk_number = models.PositiveIntegerField(
        unique=True,
        verbose_name="Номер стола",
    )

    additional_information = models.TextField(
        blank=True,
        verbose_name="Дополнительная информация",
    )

    def __str__(self):
        return f"Рабочее место №{self.desk_number}"