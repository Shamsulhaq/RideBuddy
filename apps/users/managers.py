from django.contrib.auth.models import BaseUserManager
from django.db.models import Q
from apps.permissions.choices import Roles


class UserManager(BaseUserManager):
    def create_base(
        self,
        email,
        password,
        is_staff,
        is_superuser,
        **extra_fields
    ) -> object:
        """
        Create User With Email name password
        """
        if not email:
            raise ValueError("phone is Required")

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        if user.is_superuser:
            user.role = Roles.SUPER_ADMIN
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(
        self,
        email,
        password=None,
        **extra_fields
    ) -> object:
        """Creates and save non-staff-normal user
        with given email, username and password."""

        return self.create_base(
            email,
            password,
            False,
            False,
            **extra_fields
        )

    def create_superuser(
        self,
        email,
        password,
        **extra_fields
    ) -> object:
        """Creates and saves super user
        with given email, name and password."""
        return self.create_base(
            email,
            password,
            True,
            True,
            **extra_fields
        )
    