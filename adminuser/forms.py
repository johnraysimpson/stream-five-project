from django import forms
from .models import Centre
from accounts.models import User

class CentreForm(forms.ModelForm):
    """A form for the details of a tutoring centre"""
    address1 = forms.CharField(label='Address Line 1')
    address2 = forms.CharField(label='Address Line 2', required=False)
    class Meta:
        model = Centre
        fields = [
            'centre_name',
            'address1',
            'address2',
            'town_or_city',
            'county',
            'post_code',
            'email',
            'telephone',
            ]
            
    def clean_centre_name(self):
        return self.cleaned_data['centre_name'].lower().capitalize()
        
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
        
    def clean_email(self):
        return self.cleaned_data['email'].lower()
        
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if not telephone.isdigit():
            raise forms.ValidationError("Telephone numbers should only contain numbers")
        return telephone
            
class StaffUserForm(forms.ModelForm):
    """A form for registering a staff user which asks for password confirmation"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    centre = forms.ModelChoiceField(queryset=Centre.objects.all(), empty_label="Choose Centre", to_field_name="centre_name", required=True)
    class Meta:
        model = User
        fields= ('email', 'password1', 'password2', 'centre')
        
    def clean_password2(self):
    # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(StaffUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user