from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,AbstractUser
from django.db import models
import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone number is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self,contact,name, password, **extra_fields):
        """
        Create and save a user with the contact number and password.
        """
        if not contact:
            raise ValueError(_("User must have a contact"))
        extra_fields.setdefault("is_active", True)
        user = self.model(contact=contact,name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contact,name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(contact,name,password, **extra_fields)



class User(AbstractUser):
    username=None
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,null=True,blank=True)
    contact=models.IntegerField(unique=True,primary_key=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    USERNAME_FIELD='contact'
    REQUIRED_FIELDS=['name']
    objects=CustomUserManager()
    def __str__(self) -> str:
      return str(self.contact)
    

def moderatorImgUpload(self,filename):
    return f'organization_logo/{self.organization_manager.contact}/{filename}'   



class Organization(models.Model):
   id=None
   organization_manager=models.ForeignKey(User,on_delete=models.CASCADE,related_name='organization_manager')
   working_area=models.CharField(max_length=70,null=True)
   organization_name=models.CharField(max_length=200,unique=True,primary_key=True)
   establishing_year=models.DateField()
   logo=models.ImageField(upload_to=moderatorImgUpload,null=True)
   def __str__(self) -> str:
       return self.organization_name

blood_group_choices=(
    ('1','A+'),
    ('2','A-'),
    ('3','B+'),
    ('4','B-'),
    ('5','AB-'),
    ('6','AB-'),
    ('7','O+'),
    ('8','O-')  
)

class Donar(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='donor_acount')
    district=models.CharField(max_length=50)
    upazila=models.CharField(max_length=50)
    blood_group=models.CharField(max_length=10,choices=blood_group_choices)
    last_donate=models.DateField()
    contact_number=models.IntegerField(max_length=20)
    work_for=models.CharField(max_length=100,null=True)
    def __str__(self) -> str:
        return str(self.contact_number)
    @property
    def is_capable(self):
        current=datetime.date.today()
        donate_day=self.last_donate.day
        donate_month=self.last_donate.month
        donate_year=self.last_donate.year
        delta=current - datetime.date(donate_year,donate_month,donate_day)
        return delta.days >90
    def group(self):
         if self.blood_group =='1':
             return 'A+'
         if self.blood_group =='2':
             return 'A-'
         if self.blood_group =='3':
             return 'B+'
         if self.blood_group =='4':
             return 'B-'
         if self.blood_group =='5':
             return 'AB+'
         if self.blood_group =='6':
             return 'AB-'
         if self.blood_group =='7':
             return 'O+'
         if self.blood_group =='7':
             return 'O-'
    def name(self):
        return self.user.name
    def phone_number(self):
        return '+'+ str(self.contact_number)