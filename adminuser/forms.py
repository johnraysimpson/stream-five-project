from django import forms
from .models import Centre
from accounts.models import User

class CentreForm(forms.ModelForm):
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
            
class StaffUserForm(forms.ModelForm):
    class Meta:
        model = User
        staff = forms.BooleanField(initial=True, widget=forms.HiddenInput)
        fields= ('email', 'password')