from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Prisijungimo vardas',
        max_length=50,
        error_messages={
            'required': 'Laukas yra privalomas',
            'invalid': 'Įveskite tinkamą vartotojo vardą. Naudokite raides arba skaičius.',
            'unique': 'Toks vartotojo vardas yra užimtas. Pasirinkite kitą.'
        }
    )
    email = forms.EmailField(
        label='El. paštas',
        max_length=50,
        error_messages={
            'required': 'Laukas yra privalomas',
            'invalid': 'El. paštas nėra tinkamas',
            'unique': 'Toks el. paštas yra užimtas. Pasirinkite kitą.'
        }
    )
    password1 = forms.CharField(
        label='Slaptažodis', 
        widget=forms.PasswordInput(render_value=True),
        max_length=50,
        error_messages={
            'required': 'Laukas yra privalomas',
        }
    )
    password2 = forms.CharField(
        label='Pakartokite slaptažodį', 
        widget=forms.PasswordInput(render_value=True),
        max_length=50,
        error_messages={
            'required': 'Laukas yra privalomas',
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Toks vartotojo vardas jau egzistuoja. Pasirinkite kitą.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Slaptažodžiai nesutampa.')

        return cleaned_data

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Prisijungimo vardas",
        max_length=50,
        error_messages={'required': 'Laukas yra privalomas'}
    )
    password = forms.CharField(
        label="Slaptažodis",
        widget=PasswordInput(render_value=True),
        max_length=50,
        error_messages={'required': 'Laukas yra privalomas'}
    )