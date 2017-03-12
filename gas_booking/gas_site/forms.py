from django import forms


class RegisterUserForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50)
    phone_no = forms.CharField(max_length=20)
    aadhar_no = forms.CharField(max_length=15)
    address = forms.CharField(max_length=300)
    locality = forms.CharField(max_length=50)
    district = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    pincode = forms.CharField(max_length=6)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50)


class EmailForm(forms.Form):
    e_mail = forms.EmailField(max_length=50)


class NewpasswordForm(forms.Form):
    password = forms.CharField(max_length=50)

