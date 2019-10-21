from django.db import models
from staffuser.models import TutorProfile, Student
from adminuser.models import Centre

# Create your models here.
class TutorSession(models.Model):
    """Model for session information"""
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=40)
    day = models.CharField(max_length=10)
    time = models.TimeField()
    date = models.DateField()
    duration = models.DurationField()
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    
    def __str__(self):
        return u'{0}, {1}, {2}, {3}, {4}, {5}'.format(self.subject, self.tutor.first_name, self.tutor.user.centre.centre_name, self.day, self.time, self.date)
    
class StudentSession(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sessions = models.ManyToManyField(TutorSession, blank=True)
    
    def __str__(self):
        return u"{0} {1}'s sessions".format(self.student.first_name, self.student.last_name)