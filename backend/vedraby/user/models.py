from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Электронная почта должна быть указана")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Электронная почта", unique=True)
    first_name = models.CharField("Имя", max_length=30, blank=True)
    last_name = models.CharField("Фамилия", max_length=30, blank=True)
    is_staff = models.BooleanField("Статус персонала", default=False)
    is_active = models.BooleanField("Активен", default=True)
    date_joined = models.DateTimeField("Дата регистрации", auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
