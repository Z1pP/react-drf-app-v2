from django.db import models

from vedraby.user.models import CustomUser


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    location = models.CharField(
        verbose_name="Местоположение", blank=True, null=True, max_length=100
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона", blank=True, null=True
    )
    avatar = models.ImageField("Аватар", upload_to="/avatars", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self) -> str:
        return f"Профиль пользователя {self.user.email}"
