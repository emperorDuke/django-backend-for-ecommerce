from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group

from .permissions import create_user_permissions

from BuyerProfile.models.profile import BuyerProfile


class MyUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not password:
            raise ValueError('The given password must be set')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)

        middle_name = extra_fields.get('middle_name', '')

        user_type = extra_fields.get('user_type', 'GUEST')

        if user_type != 'ADMIN' and user_type != 'GUEST':
            create_user_permissions(user_type.lower())

        user = self.model(
            email=email,
            first_name=extra_fields['first_name'],
            middle_name=middle_name,
            last_name=extra_fields['last_name'],
            phone_number=extra_fields['phone_number'],
            user_type=user_type,
            is_staff=extra_fields['is_staff'],
            is_superuser=extra_fields['is_superuser'],
            is_active=True
        )

        user.set_password(password)
        user.save(using=self._db)

        if user_type.upper() == 'SELLER':
            sellers = Group.objects.get(name='sellers')
            user.groups.add(sellers)

        if user_type.upper() == 'BUYER':
            buyers = Group.objects.get(name='buyers')
            user.groups.add(buyers)

            BuyerProfile.objects.create(user=user)

        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must = true ')

        return self._create_user(email, password, **extra_fields)
