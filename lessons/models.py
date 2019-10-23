from django.db import models
from adminuser.models import Centre

# Create your models here.
class Lesson(models.Model):
    """Model for lesson information"""
    tutor = models.ForeignKey('profiles.TutorProfile', on_delete=models.CASCADE)
    subject = models.CharField(max_length=40)
    day = models.CharField(max_length=10)
    time = models.TimeField()
    date = models.DateField()
    duration = models.DurationField()
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    
    def __str__(self):
        return u'{0}, {1}, {2}, {3}, {4}'.format(self.subject, self.centre.centre_name, self.day, self.time, self.date)