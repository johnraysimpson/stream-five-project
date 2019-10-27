from django.db import models

# Create your models here.

class Payment(models.Model):
    """A model to record any payments that have been made"""
    parent_id = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_id = models.IntegerField()
    student_first_name = models.CharField(max_length=30)
    student_last_name = models.CharField(max_length=30)
    lesson_id = models.IntegerField()
    subject = models.CharField(max_length=30)
    centre_name = models.CharField(max_length=30)
    date = models.DateField()
    amount_paid = models.DecimalField(max_digits=5, decimal_places=2)
    date_paid = models.DateField()
    
    def __str__(self):
        return u'{0}, {1}, {2}, {3}, {4}'.format(self.subject, self.date, self.student_first_name, self.date_paid, self.amount_paid)
    