from django import forms
from .models import Lesson
from profiles.models import TutorProfile, Student
import datetime
from tempus_dominus.widgets import DatePicker

def occurrence_choices():
    """Function to generate how often a lesson is required"""
    OCCURRENCE_CHOICES = [('one_off', 'One Off'), ('weekly', 'Weekly'), ('fortnightly', 'Fortnightly')]
    occurrence = forms.ChoiceField(choices=OCCURRENCE_CHOICES, widget=forms.RadioSelect())
    return occurrence

class LessonForm(forms.ModelForm):
    """Form for creating a tutor lesson"""
    DAY_CHOICES = [('', 'Choose Day'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')]
    SUBJECT_CHOICES = [('', 'Choose Subject'), ('Maths', 'Maths'), ('English', 'English'), ('Science', 'Science')]
    tutor = forms.ModelChoiceField(queryset=TutorProfile.objects.all(), empty_label="Choose Tutor", required=True)
    day = forms.ChoiceField(choices=DAY_CHOICES)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    date = forms.DateField(label="Start date", input_formats=['%d/%m/%Y'], widget=DatePicker(options={'format': 'DD/MM/YYYY', }, attrs={'input_group': False, 'autocomplete': 'off'}))
    duration = forms.DurationField(label="Duration (00:HH:MM)")
    time = forms.TimeField(label="Time (24 hour)",widget=forms.TextInput(attrs={'type': 'time'}))
    class Meta:
        model = Lesson
        fields = (
            'tutor',
            'subject',
            'day',
            'date',
            'time',
            'duration'
            )
    def clean_day(self):
        day = self.cleaned_data.get('day')
        if day == None:
            raise forms.ValidationError('Please choose a day')
        else:
            return day
            
    def clean_date(self):
        """Validation to check if the day and date matches, and if the date is not in the past"""
        input_day = self.cleaned_data.get('day')
        input_date = self.cleaned_data.get('date')
        if input_date < datetime.date.today():
            raise forms.ValidationError("Can not create a lesson in the past.")
        elif input_date.strftime("%A").lower() != input_day:
            raise forms.ValidationError(input_date.strftime("%d-%m-%Y")+" does not fall on a "+input_day.title()+".")
        return input_date
        
        

class LessonOccurrenceForm(LessonForm):
    """Form that includes occurrence field to TutorSessionForm"""
    OCCURRENCE_CHOICES = [('one_off', 'One Off'), ('weekly', 'Weekly')]
    occurrence = forms.ChoiceField(choices=OCCURRENCE_CHOICES, widget=forms.RadioSelect())
    class Meta(LessonForm.Meta):
        fields = LessonForm.Meta.fields + ('occurrence', )
        
        
class StudentToLessonForm(forms.ModelForm):
    """Form for relating a student and a lesson via the lesson"""
    student = forms.ModelChoiceField(queryset=None, empty_label="Select student", required=True)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(StudentToLessonForm, self).__init__(*args, **kwargs)
        self.fields["student"].queryset = Student.objects.filter(parent__user__centre = self.request.user.centre)
    occurrence = occurrence_choices()
    class Meta:
        model = Student
        fields = ('student', 'occurrence')
        
class LessonToStudentForm(forms.ModelForm):
    """Form for relating a student and a lesson via the student"""
    DAY_CHOICES = [('', 'Choose Day'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')]
    SUBJECT_CHOICES = [('', 'Choose Subject'), ('Maths', 'Maths'), ('English', 'English'), ('Science', 'Science')]
    tutor = forms.ModelChoiceField(queryset=TutorProfile.objects.all(), empty_label="Choose Tutor", required=True)
    day = forms.ChoiceField(choices=DAY_CHOICES)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    time = forms.TimeField(label="Time (24 hour)",widget=forms.TextInput(attrs={'type': 'time'}))
    date = forms.DateField(label="Start date", input_formats=['%d/%m/%Y'], widget=DatePicker(options={'format': 'DD/MM/YYYY', }, attrs={'input_group': False, 'autocomplete': 'off'}))
    occurrence = occurrence_choices()
    class Meta():
        model = Student
        fields = ('tutor', 'subject',  'day', 'date', 'time', 'occurrence')