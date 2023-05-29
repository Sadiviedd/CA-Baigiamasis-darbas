from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import RegisterForm, LoginAuthenticationForm


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    
    def get_success_url(self):
        return reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return redirect(self.get_success_url())


class MyLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginAuthenticationForm
    
    def get_success_url(self):
        return reverse_lazy('projects:projects-list')

    def form_invalid(self, form):
        if not form.cleaned_data.get('username') or not form.cleaned_data.get('password'):
            return super().form_invalid(form)

        messages.error(self.request, 'Netinkamas prisijungimo vardas arba slaptažodis')
        return super().form_invalid(form)