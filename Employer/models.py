from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class UserProfile(AbstractUser):
    
    COMPANY_TYPE_CHOICES = [
        ('employer_private_sector','Employer (Private Sector)'),
        ('employer_public_sector','Employer (Public Sector)'),
        ('non_proft_organization','Non-Profit Organization'),
        ('recruitment_agency','Recruitment Agency')
    ]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    last_name = models.CharField(max_length=500, blank=True)
    company_name = models.CharField(max_length=1000, blank=True)
    country = CountryField(blank=True,null=True)
    company_type = models.CharField(max_length=500, choices=COMPANY_TYPE_CHOICES, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    about_company = RichTextField(blank=True, null=True)
    company_image = models.ImageField(upload_to='RegisteredCompaniesImages/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

