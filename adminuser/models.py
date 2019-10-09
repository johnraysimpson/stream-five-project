from django.db import models

# Create your models here.
class Centre(models.Model):
    centre_name = models.CharField(max_length=30, blank=False, null=False)
    address1 = models.CharField(max_length=40, blank=False, null=False)
    address2 = models.CharField(max_length=40, blank=True, null=True)
    town_or_city = models.CharField(max_length=30, blank=False, null=False)
    county = models.CharField(max_length=30, blank=False, null=False)
    post_code = models.CharField(max_length=10, blank=False, null=False)
    email = models.EmailField(max_length=254)
    telephone = models.CharField(max_length=11, blank=False, null=False)
    