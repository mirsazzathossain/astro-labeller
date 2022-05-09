from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.forms import fields

class SignUpForm(UserCreationForm):

    input_field_style = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input appearance-none bg-transparent'

    username = forms.CharField(
        required=True,
        max_length=150,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={'unique': ("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': input_field_style, 'placeholder': ' '})
    )

    first_name = forms.CharField(
        required=True,
        max_length=12, 
        min_length=4,
        help_text='Required: First Name',
        widget=forms.TextInput(attrs={'class': input_field_style, 'placeholder': ' '})
    )

    last_name = forms.CharField(
        required=True,
        max_length=12, 
        min_length=4, 
        help_text='Required: Last Name',
        widget=forms.TextInput(attrs={'class': input_field_style, 'placeholder': ' '})
    )

    email = forms.EmailField(
        required=True,
        max_length=50, 
        help_text='Required. Inform a valid email address.',
        widget=(forms.TextInput(attrs={'class': input_field_style, 'placeholder': ' '}))
    )

    password1 = forms.CharField(
        required=True,
        widget=(forms.PasswordInput(attrs={'class': input_field_style, 'placeholder': ' '})),
        help_text=password_validation.password_validators_help_text_html()
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': input_field_style, 'placeholder': ' '}),
        help_text=('Just Enter the same password, for confirmation')
    )
    
    '''
    agree_policy = forms.ChoiceField(
        required=True,
        widget=(forms.CheckboxInput(attrs={'class': 'text-purple-600 form-checkbox focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray'}))
    )
    '''
    class Meta:
        model = get_user_model()
        fields = [
            'username', 
            'first_name',
            'last_name',
            'email', 
            'password1', 
            'password2',
        ]

class SignInForm(AuthenticationForm):
    input_field_style = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input appearance-none bg-transparent'

    username = forms.CharField(
        required=True,
        max_length=50, 
        widget=(forms.TextInput(attrs={'class': input_field_style, 'placeholder': ' ', 'id': 'username'}))
    )

    password = forms.CharField(
        required=True,
        widget=(forms.PasswordInput(attrs={'class': input_field_style, 'placeholder': ' ', 'id': 'password'})),
    )
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

