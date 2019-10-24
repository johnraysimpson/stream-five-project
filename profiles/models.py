from django.db import models
from accounts.models import User

# Create your models here.
class ParentProfile(models.Model):
    """Model for the profile of a parent user"""
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
        return u'{0} {1}'.format(self.first_name, self.last_name)
    
class TutorProfile(models.Model):
    """Model for the profile of a tutor"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address1 = models.CharField(max_length=40)
    address2 = models.CharField(max_length=40, blank=True, null=True)
    town_or_city = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    post_code = models.CharField(max_length=10)
    telephone = models.CharField(max_length=11)
    pay_per_hour = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return u'{0} {1} ({2})'.format(self.first_name, self.last_name, self.user.centre)
    
class Student(models.Model):
    """Model for student information"""
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, null=True)
    relationship = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    price_per_lesson = models.DecimalField(max_digits=4, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    lessons = models.ManyToManyField('lessons.Lesson', blank=True)
    
    def __str__(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)
        
    def get_long_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)