from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models, transaction

from apps.common.fields import IDField
from apps.common.models import AbstractBaseModel
from apps.customers.models import Profiles


class CustomerManager(BaseUserManager):
    def create_user(self, email: str, password: str, first_name: str, last_name: str, **extra_fields):
        if not email:
            raise ValueError("Email required")
        email = self.normalize_email(email)
        customer = self.model(email=email, **extra_fields)
        customer.set_password(password)

        with transaction.atomic():
            customer.save(using=self._db)
            Profiles.objects.create(
                customer=customer,
                first_name=first_name,
                last_name=last_name,
            )
        return customer

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            email,
            password,
            first_name="Admin",
            last_name="User",
            **extra_fields,
        )


class Customers(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    id = IDField()
    email = models.EmailField(max_length=128, unique=True)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomerManager()

    def __str__(self):
        return self.email
