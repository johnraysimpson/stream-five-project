from django import forms

from .models import Centre

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