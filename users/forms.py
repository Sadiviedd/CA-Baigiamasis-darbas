from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Prisijungimo vardas',
        max_length=50,
        error_messages={'required': 'Laukas yra privalomas',
                        'invalid': 'Įveskite tinkamą vartotojo vardą. Naudokite raides arba skaičius.',
                        'unique': 'Toks vartotojo vardas yra užimtas. Pasirinkite kitą.'}
    )
    email = forms.EmailField(
        label='El. paštas',
        max_length=50,
        error_messages={'required': 'Laukas yra privalomas',
                        'invalid': 'El. paštas nėra tinkamas',
                        'unique': 'Toks el. paštas yra užimtas. Pasirinkite kitą'}
    )
    password1 = forms.CharField(
        label='Slaptažodis', 
        widget=PasswordInput(render_value=True),
        max_length=50,
        error_messages={'required': 'Laukas yra privalomas',
                        'unique': 'Toks slaptažodis yra užimtas. Pasirinkite kitą'}
    )
    password2 = forms.CharField(
        label='Pakartokite slaptažodį', 
        widget=PasswordInput(render_value=True),
        max_length=50,
        error_messages={'required': 'Laukas yra privalomas',
                        'unique': ''}
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if len(password1) < 8:
            raise forms.ValidationError("Slaptažodis yra per trumpas. Turi sudaryti mažiausiai 8 simboliai.")
        elif password1 and password2 and password1 != password2:
            raise forms.ValidationError("Slaptažodžiai nesutampa.")

        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if len(password2) < 8:
            raise forms.ValidationError("Slaptažodis yra per trumpas. Turi sudaryti mažiausiai 8 simboliai.")
        elif password1 and password2 and password1 != password2:
            raise forms.ValidationError("Slaptažodžiai nesutampa.")

        return password2
    
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