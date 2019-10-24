from django import forms
from .models import ParentProfile, TutorProfile, Student

class ParentProfileForm(forms.ModelForm):
    """A form for adding profile information for the parent user that had been created on the previous page"""
    address1 = forms.CharField(label='Address Line 1')
    address2 = forms.CharField(label='Address Line 2', required=False)
    class Meta:
        model = ParentProfile
        fields = (
            'first_name',
            'last_name',
            'address1',
            'address2',
            'town_or_city',
            'county',
            'post_code',
            'telephone',
            )
    
    def clean_first_name(self):
        return self.cleaned_data['first_name'].lower().capitalize()
        
    def clean_last_name(self):
        return self.cleaned_data['last_name'].lower().capitalize()
    
    def clean_address1(self):
        return self.cleaned_data['address1'].lower().title()
        
    def clean_address2(self):
        return self.cleaned_data['address2'].lower().title()
        
    def clean_town_or_city(self):
        return self.cleaned_data['town_or_city'].lower().title()
        
    def clean_county(self):
        return self.cleaned_data['county'].lower().title()
        
    def clean_post_code(self):
        return self.cleaned_data['post_code'].upper()
        
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if not telephone.isdigit():
            raise forms.ValidationError("Telephone numbers should only contain numbers")
        return telephone
        
class TutorProfileForm(forms.ModelForm):
    """A form for adding profile information for the parent user that had been created on the previous page"""
    address1 = forms.CharField(label='Address Line 1')
    address2 = forms.CharField(label='Address Line 2', required=False)
    pay_per_hour = forms.CharField(label="Hourly rate (£)")
    class Meta:
        model = TutorProfile
        fields = (
            'first_name',
            'last_name',
            'address1',
            'address2',
            'town_or_city',
            'county',
            'post_code',
            'telephone',
            'pay_per_hour',
            )
            
    def clean_first_name(self):
        return self.cleaned_data['first_name'].lower().capitalize()
        
    def clean_last_name(self):
        return self.cleaned_data['last_name'].lower().capitalize()
    
    def clean_address1(self):
        return self.cleaned_data['address1'].lower().title()
        
    def clean_address2(self):
        return self.cleaned_data['address2'].lower().title()
        
    def clean_town_or_city(self):
        return self.cleaned_data['town_or_city'].lower().title()
        
    def clean_county(self):
        return self.cleaned_data['county'].lower().title()
        
    def clean_post_code(self):
        return self.cleaned_data['post_code'].upper()
        
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if not telephone.isdigit():
            raise forms.ValidationError("Telephone numbers should only contain numbers")
        return telephone
        
class StudentForm(forms.ModelForm):
    """Form for creating a student"""
    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
        )
    relationship = forms.CharField(label="Relationship to Student")
    class Meta:
        model = Student
        fields = ('relationship', 'first_name', 'last_name', 'date_of_birth', 'price_per_lesson', 'notes')
        
    def clean_relationship(self):
        return self.cleaned_data['relationship'].lower().capitalize()
    
    def clean_first_name(self):
        return self.cleaned_data['first_name'].lower().capitalize()
        
    def clean_last_name(self):
        return self.cleaned_data['last_name'].lower().capitalize()