from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field import formfields as phone_forms


class SignUpForm(UserCreationForm):
    contact = phone_forms.PhoneNumberField()

    class Meta:
        model = User
        fields = ('username', 'contact', 'first_name', 'last_name', 'email', 'password1', 'password2')
