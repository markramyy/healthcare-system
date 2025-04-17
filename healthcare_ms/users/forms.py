from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from healthcare_ms.users.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with additional fields specific to our User model.
    """
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
            'placeholder': _('Email address')
        })
    )
    first_name = forms.CharField(
        label=_('First Name'),
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
            'placeholder': _('First Name')
        })
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
            'placeholder': _('Last Name')
        })
    )
    phone_number = forms.CharField(
        label=_('Phone Number'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
            'placeholder': _('Phone Number')
        })
    )
    date_of_birth = forms.DateField(
        label=_('Date of Birth'),
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
        })
    )
    address = forms.CharField(
        label=_('Address'),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
            'placeholder': _('Address'),
            'rows': 3
        })
    )
    user_type = forms.ChoiceField(
        label=_('User Type'),
        choices=User.USER_TYPE_CHOICES,
        initial='patient',
        widget=forms.Select(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
        })
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'phone_number',
            'date_of_birth',
            'address',
            'user_type'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the username field
        self.fields['username'].widget.attrs.update({
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
            'placeholder': _('Username')
        })
        # Customize the password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
            'placeholder': _('Password')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm',
            'placeholder': _('Confirm Password')
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email address is already in use.'))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('This username is already taken.'))
        return username