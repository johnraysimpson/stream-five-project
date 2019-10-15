from django.db import models
from accounts.models import User

# Create your models here.
class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address1 = models.CharField(max_length=40)
    address2 = models.CharField(max_length=40, blank=True, null=True)
    town_or_city = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    post_code = models.CharField(max_length=10)
    telephone = models.CharField(max_length=11)
    
    def __str__(self):
        return u'{0}, {1}'.format(self.last_name, self.first_name)
    