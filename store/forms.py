from django import forms

class CheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=120, label="Full name")
    address = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
