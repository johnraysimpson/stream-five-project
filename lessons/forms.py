from django import forms
from .models import TutorSession, StudentSession
from staffuser.models import TutorProfile, Student



class TutorSessionForm(forms.ModelForm):
    """Form for creating a tutor session"""
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
        model = TutorSession
        fields = (
            'tutor',
            'subject',
            'day',
            'time',
            'date',
            'duration'
            )

class TutorOccurrenceSessionForm(TutorSessionForm):
    """Form that includes occurrence field to TutorSessionForm"""
    OCCURRENCE_CHOICES = [('one_off', 'One Off'), ('weekly', 'Weekly')]
    occurrence = forms.ChoiceField(choices=OCCURRENCE_CHOICES, widget=forms.RadioSelect())
    class Meta(TutorSessionForm.Meta):
        fields = TutorSessionForm.Meta.fields + ('occurrence', )
        
        
class StudentSessionForm(forms.ModelForm):
    """Form for creating a student session"""
    student = forms.ModelChoiceField(queryset=None, empty_label="Choose student", required=True)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(StudentSessionForm, self).__init__(*args, **kwargs)
        self.fields["student"].queryset = Student.objects.filter(parent__user__centre = self.request.user.centre)
    class Meta:
        model = StudentSession
        fields = ('student',)
        
class SessionMatchForm(StudentSessionForm):
    """extends student session form to find corresponding tutor sessions"""
    DAY_CHOICES = [('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')]
    SUBJECT_CHOICES = [('maths', 'Maths'), ('english', 'English'), ('science', 'Science')]
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
    class Meta(StudentSessionForm.Meta):
        fields = StudentSessionForm.Meta.fields + ('tutor', 'day', 'subject', 'time', 'date', 'occurrence')