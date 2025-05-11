# users/forms.py
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .models import UserProfile

class PhoneNumberForm(forms.Form):
    # ... (мурункудай калат) ...
    phone_number = forms.CharField(
        label="Телефон номериңиз",
        validators=[RegexValidator(regex=r'^(\+996|0)\d{9}$', message="...")],
        # widget атрибутун алып салсак, CSS менен оңой башкарабыз
    )

class OTPVerificationForm(forms.Form):
    # ... (мурункудай калат) ...
    otp_code = forms.CharField(
        label="SMS аркылуу келген код",
        max_length=6,
        min_length=6,
    )

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False, label="Электрондук почта")
    username = forms.CharField(label="Колдонуучу аты", help_text="Талап кылынат. 150 же аз арип, сан жана @/./+/-/_ лар гана.")

    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'bio', 'profile_picture', 'date_of_birth']
        # Виджеттерди алып салдык, JavaScript менен тууралайбыз же CSS менен
        # labels = { 'first_name': 'Атыңыз' } сыяктуу label'дарды өзгөртсөңүз болот