from django import forms
from gas_site.models import User


class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']


class UpdateDetailsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_no', 'aadhar_no', 'gender', 'house_name',
                  'street', 'city', 'state', 'pin_code']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50)


class EmailForm(forms.Form):
    e_mail = forms.EmailField(max_length=50)


class NewpasswordForm(forms.Form):
    password = forms.CharField(max_length=50)

