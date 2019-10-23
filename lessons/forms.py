from django import forms
from .models import Lesson
from profiles.models import TutorProfile, Student
import datetime



class LessonForm(forms.ModelForm):
    """Form for creating a tutor lesson"""
    DAY_CHOICES = [('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')]
    SUBJECT_CHOICES = [('maths', 'Maths'), ('english', 'English'), ('science', 'Science')]
    tutor = forms.ModelChoiceField(queryset=TutorProfile.objects.all(), empty_label="Choose Tutor", required=True)
    day = forms.ChoiceField(choices=DAY_CHOICES)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    time = forms.TimeField(widget=forms.TimeInput(format="%H:%M"))
    date = forms.DateField(label="Start date",
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
        )
    
    class Meta:
        model = Lesson
        fields = (
            'tutor',
            'subject',
            'day',
            'time',
            'date',
            'duration'
            )
            
    def clean_date(self):
        input_day = self.cleaned_data.get('day')
        input_date = self.cleaned_data.get('date')
        print(input_date)
        print(input_day)
        if input_date.strftime("%A").lower() != input_day:
            raise forms.ValidationError(input_date.strftime("%d-%m-%Y")+" does not fall on a "+input_day.capitalize()+".")
        elif input_date < datetime.date.today():
            raise forms.ValidationError("Can not create a lesson in the past.")
        return input_date
        
    def clean_subject(self):
        return self.cleaned_data['subject'].lower().title()

class LessonOccurrenceForm(LessonForm):
    """Form that includes occurrence field to TutorSessionForm"""
    OCCURRENCE_CHOICES = [('one_off', 'One Off'), ('weekly', 'Weekly')]
    occurrence = forms.ChoiceField(choices=OCCURRENCE_CHOICES, widget=forms.RadioSelect())
    class Meta(LessonForm.Meta):
        fields = LessonForm.Meta.fields + ('occurrence', )
        
        
class StudentLessonForm(forms.ModelForm):
    """Form for creating a student session"""
    student = forms.ModelChoiceField(queryset=None, empty_label="Choose student", required=True)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(StudentLessonForm, self).__init__(*args, **kwargs)
        self.fields["student"].queryset = Student.objects.filter(parent__user__centre = self.request.user.centre)
    class Meta:
        model = Student
        fields = ('student',)
        
class LessonMatchForm(StudentLessonForm):
    """extends student session form to find corresponding tutor sessions"""
    DAY_CHOICES = [('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')]
    SUBJECT_CHOICES = [('Maths', 'Maths'), ('English', 'English'), ('Science', 'Science')]
    OCCURRENCE_CHOICES = [('one_off', 'One Off'), ('weekly', 'Weekly'), ('fortnightly', 'Fortnightly')]
    tutor = forms.ModelChoiceField(queryset=TutorProfile.objects.all(), empty_label="Choose Tutor", required=True)
    day = forms.ChoiceField(choices=DAY_CHOICES)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    time = forms.TimeField(widget=forms.TimeInput(format="%H:%M"))
    date = forms.DateField(label="Start date",
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
        )
    occurrence = forms.ChoiceField(choices=OCCURRENCE_CHOICES, widget=forms.RadioSelect())
    class Meta(StudentLessonForm.Meta):
        fields = StudentLessonForm.Meta.fields + ('tutor', 'day', 'subject', 'time', 'date', 'occurrence')