from django import forms
from accounts.models import User
from .models import ParentProfile

class ParentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ParentUserForm, self).save(commit=False)
        password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        print(password) #delete this when email is set up
        user.set_password(password)
        if commit:
            user.save()
        return user
        
class ParentProfileForm(forms.ModelForm):
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