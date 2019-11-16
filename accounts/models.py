from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from adminuser.models import Centre

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """A custom user model"""
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    parent = models.BooleanField(default=False)
    tutor = models.BooleanField(default=False)
    password_changed = models.BooleanField(default=False)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE, default=None, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Function for determining if a user has a permission"""
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Function for determining if a user has permissions to view apps"""
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_parent(self):
        """Function for determining if a user is a member of staff"""
        "Is the user a member of staff?"
        return self.parent
    
    @property
    def is_tutor(self):
        """Function for determining if a user is a tutor"""
        "Is the user a member of staff?"
        return self.tutor
    
    @property
    def is_staff(self):
        """Function for determining if a user is a parent"""
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        """Function for determining if a user is an admin"""
        "Is the user a admin member?"
        return self.admin
        
    objects = UserManager()