from django import forms
from datetime import datetime

def this_year():
    todays_date = datetime.today()
    this_year = todays_date.year
    return this_year

class MakePaymentForm(forms.Form):
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(this_year(), this_year() + 19)]
    
    credit_card_number = forms.CharField(label='Credit Card Number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices = MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices = YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)