from django import forms
from .models import Lesson
from profiles.models import TutorProfile, Student
import datetime

def occurrence_choices():
    """Function to generate how often a lesson is required"""
    OCCURRENCE_CHOICES = [('one_off', 'One Off'), ('weekly', 'Weekly'), ('fortnightly', 'Fortnightly')]
    occurrence = forms.ChoiceField(choices=OCCURRENCE_CHOICES, widget=forms.RadioSelect())
    return occurrence

class LessonForm(forms.ModelForm):
    """Form for creating a tutor lesson"""
    DAY_CHOICES = [('', 'Choose Day'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')]
    SUBJECT_CHOICES = [('', 'Choose Subject'), ('maths', 'Maths'), ('english', 'English'), ('science', 'Science')]
    tutor = forms.ModelChoiceField(queryset=TutorProfile.objects.all(), empty_label="Choose Tutor", required=True)
    day = forms.ChoiceField(choices=DAY_CHOICES)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    time = forms.TimeField(label="Time (24 hour)",widget=forms.TextInput(attrs={'type': 'time'}))
    date = forms.DateField(label="Start date", widget=forms.TextInput(attrs={'type': 'date'},))
    duration = forms.DurationField(label="Duration (00:HH:MM)")
    
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
        print(input_date)
        print(input_day)
        if input_date < datetime.date.today():
            raise forms.ValidationError("Can not create a lesson in the past.")
        elif input_date.strftime("%A").lower() != input_day:
            raise forms.ValidationError(input_date.strftime("%d-%m-%Y")+" does not fall on a "+input_day.title()+".")
        return input_date
        
    def clean_subject(self):
        input_subject = self.cleaned_data['subject']
        if input_subject == "":
            raise forms.ValidationError("Please choose a subject")
        else:
            return self.cleaned_data['subject'].lower().title()

class LessonOccurrenceForm(LessonForm):
    """Form that includes occurrence field to TutorSessionForm"""
    OCCURRENCE_CHOICES = [('one_off', 'One Off'), ('weekly', 'Weekly')]
    occurrence = occurrence_choices()
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
    DAY_CHOICES = [('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')]
    SUBJECT_CHOICES = [('Maths', 'Maths'), ('English', 'English'), ('Science', 'Science')]
    tutor = forms.ModelChoiceField(queryset=TutorProfile.objects.all(), empty_label="Choose Tutor", required=True)
    day = forms.ChoiceField(choices=DAY_CHOICES)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    time = forms.TimeField(label="Time (24 hour)",widget=forms.TextInput(attrs={'type': 'time'}))
    date = forms.DateField(label="Start date", widget=forms.TextInput(attrs={'type': 'date'},))
    occurrence = occurrence_choices()
    class Meta():
        model = Student
        fields = ('tutor', 'day', 'subject', 'date', 'time', 'occurrence')