from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from django.core.validators import RegexValidator
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
    email = models.EmailField(
        _('Email Address'), max_length=255, unique=True, blank=False, null=True
    )

    phone = models.CharField(
        _('Mobile Phone'), max_length=12, blank=True, null=True,
        validators=[RegexValidator(r'^[\d]{10,12}$',
                                   message='Format (ex: 0123456789)'
                                   )])

    first_name = models.CharField(
        _('First Name'), max_length=255, blank=True, null=True
    )

    last_name = models.CharField(
        _('Last Name'), max_length=255, blank=True, null=True
    )
    
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission? yes."
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`? yes."
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, unique=True
    )
    image = models.ImageField(
        _('Profile Picture'), blank=True, null=True,
        upload_to=user_directory_path
    )
    bio = models.TextField(
        _('Bio'), blank=True, null=True
    )
    birthday = models.DateField(
        _('Date of Birth'), blank=True, null=True
    )
    gender = models.CharField(
        _('Gender'), max_length=1, blank=True, null=True,
        choices=[('M', 'Male'), ('F', 'Female')]
    )

    available_Balance = models.IntegerField( default = True, null= True)

    is_active = models.BooleanField(
        _('Active'), default=True, null=True
    )
    created_at = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Creates or updates profile, when User object changes"""
    if created:
        Profile.objects.get_or_create(user=instance)
    instance.profile.save()


class event(models.Model):
    id = models.AutoField
    lotteryNumber = models.BigIntegerField(null=True, unique=True)
    start_time = models.DateTimeField(auto_now_add=True, editable=False)
    end_time = models.DateTimeField(null=True)
    blue_count = models.IntegerField(default=0)
    green_count = models.IntegerField(default=0)
    red_count = models.IntegerField(default=0)

    zero_count = models.IntegerField(default=0)
    one_count = models.IntegerField(default=0)
    two_count = models.IntegerField(default=0)
    three_count = models.IntegerField(default=0)
    four_count = models.IntegerField(default=0)
    five_count = models.IntegerField(default=0)
    six_count = models.IntegerField(default=0)
    seven_count = models.IntegerField(default=0)
    eight_count = models.IntegerField(default=0)
    nine_count = models.IntegerField(default=0)


    def __str__(self):
        return str(self.lotteryNumber)

class transaction(models.Model):
    # choice = ('Red', 'Green', 'Blue')
    id = models.AutoField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    colour = models.CharField(choices=[('Red', 'Red'), ('Green', 'Green'), ('Blue', 'Blue')], max_length=5, blank=True)
    luckyNumber = models.IntegerField(default=0)
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.CharField(null= True, max_length=8)
    


class finalResult(models.Model):
    event = models.OneToOneField(event, on_delete=models.CASCADE, unique=True, primary_key= True)
    colour = models.CharField(max_length = 5)
    luckyNumber = models.IntegerField(default=0)

    def __str__(self):
        return str(self.event)



class PaymentPartner(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=20, null=True)
    email = models.EmailField(
        _('Email Address'), max_length=255, unique=True, blank=False, null=True
    )

    phone = models.CharField(
        _('Mobile Phone'), max_length=12, blank=True, null=True,
        validators=[RegexValidator(r'^[\d]{10,12}$',
                                   message='Format (ex: 0123456789)'
                                   )])
    alternateNumber = models.CharField(
        _('Alternate number'), max_length=12, blank=True, null=True,
        validators=[RegexValidator(r'^[\d]{10,12}$',
                                   message='Format (ex: 0123456789)'
                                   )])
    upiId = models.CharField(max_length= 20, blank=True, null= True)

    def __str__(self):
        return self.name


class PaymentRecord(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20, null=True)
    email = models.EmailField(
        _('Email Address'), max_length=255, unique=False, blank=False, null=True
    )

    phone = models.CharField(
        _('Mobile Phone'), max_length=12, blank=True, null=True,
        validators=[RegexValidator(r'^[\d]{10,12}$',
                                   message='Format (ex: 0123456789)'
                                   )])
    rechargeAmount = models.IntegerField()

    paymentSentTo = models.ForeignKey(PaymentPartner, on_delete=models.SET_DEFAULT, default=None, null=True)

    UTR_num = models.CharField(max_length= 30, unique=True)

    status = models.CharField(max_length=20, null= True)


class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=(('UPI', 'UPI'), ('Bank', 'Bank')))
    account_number = models.CharField(max_length=20, null=True, blank=True)
    account_holder_name = models.CharField(max_length=50, null=True, blank=True)
    UPI_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
