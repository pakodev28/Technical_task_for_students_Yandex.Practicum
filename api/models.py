from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()

PHONE_VALIDATOR = RegexValidator(
    regex=r"^\+(?:[0-9] ?){6,14}[0-9]$",
    message="Phone number must be entered in the E.123 format.",
)


class Organization(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organizations"
    )
    editors = models.ManyToManyField(User, through="EditingRight")
    name = models.CharField(
        max_length=256, unique=True, verbose_name="Название"
    )
    address = models.CharField(
        max_length=256,
        verbose_name="Адрес",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание"
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


class EditingRight(models.Model):
    editor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="editing_rights",
        verbose_name="Пользователь с правом редактирования",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name="Организация",
        related_name="editing_rights",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["editor", "organization"], name="org_editors"
            )
        ]
        ordering = ("editor",)
        verbose_name = "Право на редактирование"
        verbose_name_plural = "Права на редактирование"

    def __str__(self):
        return "{}. {} может изменять данные {}".format(
            self.id, self.editor, self.organization
        )


class Worker(models.Model):
    full_name = models.CharField(max_length=60, verbose_name="ФИО")
    position = models.CharField(max_length=256, verbose_name="Должность")
    work_number = models.CharField(
        max_length=15,
        validators=[PHONE_VALIDATOR],
        blank=True,
        null=True,
        verbose_name="Рабочий номер телефона",
    )
    private_number = models.CharField(
        max_length=15,
        validators=[PHONE_VALIDATOR],
        blank=True,
        null=True,
        unique=True,
        verbose_name="Личный номер телефона",
    )
    fax = models.CharField(
        max_length=15,
        validators=[PHONE_VALIDATOR],
        blank=True,
        null=True,
        verbose_name="Факс",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="workers",
        verbose_name="Организация",
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def clean(self):
        if (
            self.work_number is None
            and self.private_number is None
            and self.fax is None
        ):
            raise ValidationError("Нужно указать хотя бы один номер телефона")

    def __str__(self):
        return self.full_name
