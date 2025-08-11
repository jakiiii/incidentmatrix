import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None, is_active=True, is_staff=False,
                    is_superuser=False, is_administrator=False, is_operator=False):
        if not first_name:
            raise ValueError("Please, type your first name.")
        if not last_name:
            raise ValueError("Please type your last name.")
        if not username:
            raise ValueError('User have to an username address!')
        if not password:
            raise ValueError('User must have a password!')
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.is_administrator = is_administrator
        user.is_operator = is_operator
        user.save(using=self._db)
        return user

    def create_staff(self, username, first_name, last_name, password=None):
        user = self.create_user(
            username,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        return user

    def create_superuser(self, username, first_name, last_name, password=None):
        user = self.create_user(
            username,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_superuser=True,
            is_administrator=True,
            is_operator=True,
        )
        return user


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email Address"),
        db_collation='und-x-icu',
    )
    is_administrator = models.BooleanField(
        default=False,
        verbose_name=_("Is Administrator"),
    )
    is_operator = models.BooleanField(
        default=False,
        verbose_name=_("Is Operator"),
    )
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "tbl_user"
