from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from gas_site.validators import *
from gas_site.managers import *


class User(AbstractBaseUser):

    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Consumer'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unspecified')
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    consumer_id = models.CharField(max_length=8, null=True, blank=True)

    phone_no = models.CharField(validators=[phone_validator], max_length=17, null=True, blank=True)
    aadhar_no = models.CharField(validators=[aadhar_validator], max_length=12, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    house_name = models.CharField(max_length=300, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pin_code = models.CharField(max_length=6, null=True, blank=True)

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_no']

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._password = None

    def __str__(self):
        return str(self.id) + '. ' + self.get_full_name()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.role == 1

    @property
    def is_staff(self):
        return self.role == 1

    def has_perm(self, perm, obj=None):
        return self.role == 1

    def has_module_perms(self, app_label):
        return self.role == 1

    def delete(self, *args, **kwargs):
        self.is_active = False
        return self


class UserRequests(models.Model):

    NEW_REQUEST = 'NEW'
    REFIL = 'RFL'
    SURRENDER = 'SDR'

    TYPE = (
        (NEW_REQUEST, 'New Request'),
        (REFIL, 'Refill'),
        (SURRENDER, 'Surrender')
    )

    NOT_PROCESSED = 'NPR'
    PROCESSING = 'PRG'
    REJECTED = 'RJT'
    COMPLETED = 'CMP'

    STATUS = (
        (NOT_PROCESSED, 'Not Processed'),
        (PROCESSING, 'Processing'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed')
    )
    user = models.ForeignKey(User)
    type = models.CharField(max_length=3, choices=TYPE)
    request_date = models.DateTimeField(auto_now_add=True)
    expected_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=3, choices=STATUS, default=NOT_PROCESSED)   

    def __str__(self):
        return "%s" % self.consumer_id
