

from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Employee(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
    )
    hire_date = models.DateField(
        verbose_name='Дата приёма на работу',
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=20,
        verbose_name='Пол',
    )
    skills = models.TextField(
        verbose_name='Навыки',
    )
    workplace = models.ForeignKey(
    'workplaces.Workplace',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='employees',
    verbose_name='Рабочее место',
)

    def clean(self):
        super().clean()

        if not self.workplace_id or not self.skills:
            return

        skills = self.skills.lower()

        is_tester = any(
            word in skills
            for word in ('тестировщик', 'tester', 'qa')
        )
        is_developer = any(
            word in skills
            for word in (
                'бекендер',
                'бэкендер',
                'backend',
                'фронтендер',
                'frontend',
                'разработчик',
            )
        )

        if not (is_tester or is_developer):
            return

        neighbour_employees = Employee.objects.filter(
            workplace__desk_number__in=[
                self.workplace.desk_number - 1,
                self.workplace.desk_number + 1,
            ]
        ).exclude(pk=self.pk)

        for neighbour in neighbour_employees:
            neighbour_skills = (neighbour.skills or '').lower()

            neighbour_is_tester = any(
                word in neighbour_skills
                for word in ('тестировщик', 'tester', 'qa')
            )
            neighbour_is_developer = any(
                word in neighbour_skills
                for word in (
                    'бекендер',
                    'бэкендер',
                    'backend',
                    'фронтендер',
                    'frontend',
                    'разработчик',
                )
            )

            if (
                is_tester and neighbour_is_developer
            ) or (
                is_developer and neighbour_is_tester
            ):
                raise ValidationError({
                    'workplace': (
                        'Тестировщик и разработчик '
                        'не могут сидеть за соседними столами.'
                    )
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Сотрудник',
    )
    image = models.ImageField(
        upload_to='employees/',
        verbose_name='Фотография',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядковый номер',
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.employee} — фото {self.order}'


@receiver(post_delete, sender=EmployeeImage)
def delete_employee_image(sender, instance, **kwargs):
    if instance.image:
        image_path = Path(instance.image.path)

        if image_path.exists():
            image_path.unlink()