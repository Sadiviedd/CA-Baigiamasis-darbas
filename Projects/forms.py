from django import forms
from .models import Projects, Customers, Project_Expenditures, Project_jobs, Invoices, Invoice_payments, Project_Constructions, Project_Status


class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['customer_id'].queryset = self.fields['customer_id'].queryset.filter(user=user)
            self.fields['construction_id'].queryset = self.fields['construction_id'].queryset.filter(user=user)
            self.fields['status_id'].queryset = self.fields['status_id'].queryset.filter(user=user)
    
    class Meta:
        model = Projects
        exclude = ['user', 'create_date', 'update_date']
        labels = {
            'project_name': 'Projektas',
            'customer_id': 'Klientas',
            'address': 'Adresas',
            'mobile_number': 'Tel. Nr.',
            'country': 'Šalis',
            'city': 'Miestas',
            'email': 'El. paštas',
            'construction_id': 'Konstrukcija',
            'kw': 'KW',
            'modules_w': 'Moduliai, W',
            'status_id': 'Projekto būsena',
            'subcontracting': 'Subrangos montuotojai',
            'eur_kw': 'EUR/KW',
            'comment': 'Komentaras',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Rašykite čia..', 'style': 'max-width: 300px; max-height: 100px;'}),
        }


class ProjectUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['construction_id'].queryset = self.fields['construction_id'].queryset.filter(user=user)
            self.fields['status_id'].queryset = self.fields['status_id'].queryset.filter(user=user)

    class Meta:
        model = Projects
        exclude = ['user', 'create_date', 'update_date']
        labels = {
            'project_name': 'Projektas',
            'address': 'Adresas',
            'country': 'Šalis',
            'city': 'Miestas',
            'construction_id': 'Konstrukcija',
            'kw': 'KW',
            'modules_w': 'Moduliai, W',
            'status_id': 'Projekto būsena',
            'subcontracting': 'Subrangos montuotojai',
            'eur_kw': 'EUR/KW',
            'comment': 'Komentaras',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Rašykite čia..', 'style': 'max-width: 300px; max-height: 100px;'}),
        }
        fields = ['project_name', 'address', 'country', 'city', 'construction_id', 'kw', 'modules_w', 'status_id', 'subcontracting', 'eur_kw', 'comment']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude = ['user', 'customer_id']
        labels = {
            'name': 'Vardas',
            'surname': 'Pavardė',
            'email': 'El. paštas',
            'mobile_number': 'Tel. Nr.',
            'term_days': 'Terminas (dienomis)',
        }
        fields = ['name', 'surname', 'email', 'mobile_number', 'term_days']


class InvoicesCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project_id'].queryset = self.fields['project_id'].queryset.filter(user=user)

    class Meta:
        model = Invoices
        fields = ['invoice_no', 'project_id', 'operation_date', 'term_days', 'amount']
        labels = {
            'invoice_no': 'Sąskaitos nr.',
            'project_id': 'Projektas',
            'operation_date': 'Pridėjimo data',
            'term_days': 'Terminas (dienomis)',
            'amount': 'Suma, eur'
        }
        widgets = {
            'operation_date': DateInput(),
        }


class InvoicesUpdateForm(forms.ModelForm):
    class Meta:
        model = Invoices
        fields = ['invoice_no', 'operation_date', 'term_days', 'amount']
        labels = {
            'invoice_no': 'Sąskaitos nr.',
            'operation_date': 'Pridėjimo data',
            'term_days': 'Terminas (dienomis)',
            'amount': 'Suma, eur'
        }
        widgets = {
            'operation_date': DateInput(),
        }


class InvoicePaymentsCreateForm(forms.ModelForm):
    class Meta:
        model = Invoice_payments
        fields = ['payment_date', 'paid_amount']
        labels = {
            'payment_date': 'Apmokėjimo data',
            'paid_amount': 'Apmokėta suma, eur',
        }
        widgets = {
            'payment_date': DateInput(),
        }


class ExpendituresCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project_id'].queryset = self.fields['project_id'].queryset.filter(user=user)

    class Meta:
        model = Project_Expenditures
        fields = ['project_id', 'name', 'quantity', 'price']
        labels = {
            'project_id': 'Projektas',
            'name': 'Išlaidos pavadinimas',
            'quantity': 'Kiekis',
            'price': 'Kaina',
        }


class ExpendituresUpdateForm(forms.ModelForm):
    class Meta:
        model = Project_Expenditures
        fields = ['name', 'quantity', 'price']
        labels = {
            'name': 'Išlaidos pavadinimas',
            'quantity': 'Kiekis',
            'price': 'Kaina',
        }


class ProjectJobsCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project_id'].queryset = self.fields['project_id'].queryset.filter(user=user)
    
    class Meta:
        model = Project_jobs
        exclude = ['user', 'neto_time', 'isDone']
        labels = {
            'project_id': 'Projektas',
            'title': 'Darbo pavadinimas',
            'start_date': 'Pradžios data',
            'end_date': 'Pabaigos data',
            'work_time': 'Darbo trukmė, val.',
            'break_time': 'Pertrauka, val.',
        }
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }


class ProjectJobsUpdateForm(forms.ModelForm):
    class Meta:
        model = Project_jobs
        exclude = ['user', 'neto_time', 'project_id', 'isDone']
        labels = {
            'title': 'Darbo pavadinimas',
            'start_date': 'Pradžios data',
            'end_date': 'Pabaigos data',
            'work_time': 'Darbo trukmė, val.',
            'break_time': 'Pertrauka, val.',
        }
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }


class ConstructionForm(forms.ModelForm):
    class Meta:
        model = Project_Constructions
        fields = ['name']


class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = Project_Status
        fields = ['name']