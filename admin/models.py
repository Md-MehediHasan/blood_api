from django.contrib.auth.models import AbstractUser
from django.db import models


def moderatorImgUpload(self,filename):
    return f'{self.organization_name}/{filename}'
class Moderator(AbstractUser):
    email=models.EmailField(max_length=100)
    contact=models.IntegerField()
    organization_name=models.CharField(max_length=200,unique=True)
    establishing_year=models.IntegerField()
    logo=models.ImageField(upload_to=moderatorImgUpload,null=True)
    USERNAME_FIELD='organization_name'
    REQUIRED_FIELDS=['email','contact','establishing_year']


