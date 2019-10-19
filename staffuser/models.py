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
        return u'{0}, {1}'.format(self.last_name, self.first_name)
    
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
        
class TutorSession(models.Model):
    """Model for session information"""
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=40)
    day = models.CharField(max_length=10)
    time = models.TimeField()
    date = models.DateField()
    duration = models.DurationField()
    
    def __str__(self):
        return u'{0}, {1}, {2}, {3}, {4}, {5}'.format(self.subject, self.tutor.first_name, self.tutor.user.centre.centre_name, self.day, self.time, self.date)
    
class Student(models.Model):
    """Model for student information"""
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    notes = models.TextField()