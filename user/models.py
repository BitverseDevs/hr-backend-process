from django.db import models
from django.core.validators import MaxValueValidator

EMPLOYEE_ID_MAX = 9990
USERNAME_LENGTH_MAX = 9
ROLE_CHOICES = (
        (1, 'employee'),
        (2, 'hr_staff'),
        (3, 'hr_admin'),
        (4, 'hr_superadmin'),
        (5, 'developer'),
    )

class User(models.Model):
    
    employee_id = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(EMPLOYEE_ID_MAX)])
    username = models.CharField(max_length=USERNAME_LENGTH_MAX)
    password = models.CharField(max_length=128)
    date_added = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    date_deleted = models.DateTimeField(blank=True, null=True)
    is_locked = models.BooleanField(default=False)

    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    
    old_password = models.CharField(max_length=128, blank=True, default=0)
    date_password_change = models.DateTimeField(blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
    


















# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from django.utils import timezone
# from django.core.validators import MinValueValidator, MaxValueValidator
# class Roles(models.TextChoices):
#     employee = 1,
#     hr_staff = 2,
#     hr_admin = 3,
#     hr_superadmin = 4,
#     developer = 5

# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None):
#         if not username:
#             raise ValueError("User must have a username")
        
#         user = self.model(username=username)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user
    
#     def create_staff(self, username, password, **extra_fields):
#         extra_fields.setdefault("role", Roles.employee)
#         extra_fields.setdefault("is_active", True)

#         if extra_fields.get("role") != Roles.employee:
#             raise ValueError(_("Staff must have role=staff"))
        
#         return self.create_user(username=username, password=password, **extra_fields)

# class CustomUser(AbstractBaseUser):
#     employee_no = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="employee number")
#     username = models.CharField(max_length=8, unique=True)
#     password = models.CharField(max_length=64)
#     old_password = models.CharField(max_length=64)

#     date_added = models.DateField(default=timezone.now)
#     date_deleted = models.DateField()
#     date_pw_change = models.DateField(verbose_name="date password change")
#     login_attempts = models.PositiveSmallIntegerField()

#     is_active = models.BooleanField(default=True)
#     is_locked = models.BooleanField(default=False)
#     role = models.IntegerField(choices=Roles.choices, default=Roles.employee)
    
    # 1 = Developer everything all
    # 2 = HR SuperAdmin data maintenance 
    # 3 = HR Admin approver, hr staff hr admin, employee edit request
    # 4 = HR Staff file leave for other employee
    # 5 = Employee view edit profile

    # USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = []
    # objects = UserManager()

    # def __str__(self):
    #     return self.username
    
    # def has_perm(self, perm, obj=None):
    #     return True
    
    # def has_module_perms(self, app_label):
    #     return True
    
    # @property
    # def _role(self):
    #     return self.role