from django.db import models

# Create your models here.
class Centre(models.Model):
    """The model for a centre and it's details"""
    centre_name = models.CharField(max_length=30)
    address1 = models.CharField(max_length=40)
    address2 = models.CharField(max_length=40, blank=True, null=True)
    town_or_city = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    post_code = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    telephone = models.CharField(max_length=11)
    
    def __str__(self):
        return u'{0}'.format(self.centre_name)