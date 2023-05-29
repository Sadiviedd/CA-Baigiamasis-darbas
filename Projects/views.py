from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import (
        ProjectCreateForm,
        ProjectUpdateForm,
        ConstructionForm,
        ProjectStatusForm,
        CustomerForm,
        ExpendituresCreateForm,
        ExpendituresUpdateForm,
        ProjectJobsCreateForm,
        ProjectJobsUpdateForm,
        InvoicesCreateForm,
        InvoicesUpdateForm,
        InvoicePaymentsCreateForm)
from .models import Projects, Customers, Project_Expenditures, Project_jobs, Invoices, Invoice_payments, Project_Constructions, Project_Status
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q


def project_detail_view(request, pk):
    projects = Projects.objects.filter(user=request.user, project_id=pk)
    jobs = Project_jobs.objects.filter(user=request.user, project_id=pk)
    invoices = Invoices.objects.filter(user=request.user, project_id=pk)
    expenditures = Project_Expenditures.objects.filter(user=request.user, project_id=pk)

    context = {
        'projects': projects,
        'jobs': jobs,
        'invoices': invoices,
        'expenditures': expenditures,
    }
    return render(request, 'Projects/project_details.html', context)


# PROJEKTU LIST'AS
class ProjectsListView(LoginRequiredMixin, ListView):
    model = Projects
    template_name = 'Projects/projects_list.html'
    context_object_name = 'projects'
    login_url = '/login/'
    paginate_by = 15
    ordering = 'project_name'

    def get_queryset(self):
        return Projects.objects.filter(user=self.request.user)


# PROJEKTO SUKURIMAS
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Projects
    form_class = ProjectCreateForm
    template_name = 'Projects/projects_create.html'
    success_url = reverse_lazy('projects:projects-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# PROJEKTO ATNAUJINIMAS
class ProjectsUpdateView(LoginRequiredMixin, UpdateView):
    model = Projects
    form_class = ProjectUpdateForm
    template_name = 'Projects/projects_update.html'

    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    def get_success_url(self):
        if 'last_visited_url' in self.request.session:
            return self.request.session['last_visited_url']
        else:
            return reverse('projects:projects-list')

    def get(self, request, *args, **kwargs):
        self.request.session['last_visited_url'] = self.request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)


# PROJEKTO ISTRYNIMAS
@login_required(login_url='/login/')
def ProjectsDelete(request, pk):
    project = Projects.objects.get(project_id=pk)
    project.delete()
    return redirect('projects:projects-list')


# KLIENTU LIST'AS
class CustomersListView(LoginRequiredMixin, ListView):
    model = Customers
    template_name = 'Projects/customers_list.html'
    context_object_name = 'customers'
    login_url = '/login/'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(surname__icontains=search_query)
            )
        self.request.session['filtered_customer_search'] = search_query
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.session.get('filtered_customer_search', '')
        return context


# KLIENTO SUKURIMAS
class CustomersCreateView(LoginRequiredMixin, CreateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'Projects/customers_create.html'
    success_url = reverse_lazy('projects:customers-list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# KLIENTO ATNAUJINIMAS
class CustomersUpdateView(LoginRequiredMixin, UpdateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'Projects/customers_update.html'
    success_url = reverse_lazy('projects:customers-list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


# KLIENTO ISTRYNIMAS
@login_required(login_url='/login/')
def CustomerDelete(request, pk):
    customer = Customers.objects.get(customer_id=pk)
    customer.delete()
    return redirect('projects:customers-list')


# ISLAIDU LIST'AS
class ExpendituresListView(LoginRequiredMixin, ListView):
    model = Project_Expenditures
    template_name = 'Projects/expenditures_list.html'
    context_object_name = 'expenditures'
    login_url = '/login/'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(project_id__project_name__icontains=search_query)
            )
        self.request.session['filtered_expenditure_search'] = search_query
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.session.get('filtered_expenditure_search', '')
        return context


# ISLAIDU SUKURIMAS
class ExpendituresCreateView(LoginRequiredMixin, CreateView):
    model = Project_Expenditures
    form_class = ExpendituresCreateForm
    template_name = 'Projects/expenditures_create.html'
    success_url = reverse_lazy('projects:expenditures-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ISLAIDU ATNAUJINIMAS
class ExpendituresUpdateView(LoginRequiredMixin, UpdateView):
    model = Project_Expenditures
    form_class = ExpendituresUpdateForm
    template_name = 'Projects/expenditures_update.html'
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    def get_success_url(self):
        if 'last_visited_url' in self.request.session:
            return self.request.session['last_visited_url']
        else:
            return reverse('projects:expenditures-list')

    def get(self, request, *args, **kwargs):
        self.request.session['last_visited_url'] = self.request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)


# ISLAIDU ISTRYNIMAS
def ExpendituresDelete(request, pk):
    expenditures = Project_Expenditures.objects.get(id=pk)
    request.session['last_visited_url'] = request.META.get('HTTP_REFERER')
    expenditures.delete()
    if 'last_visited_url' in request.session:
        return redirect(request.session['last_visited_url'])
    else:
        return redirect('projects:expenditures-list')


# DARBU LIST'AS
class JobsListView(LoginRequiredMixin, ListView):
    model = Project_jobs
    template_name = 'Projects/jobs_list.html'
    context_object_name = 'jobs'
    login_url = '/login/'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(project_id__project_name__icontains=search_query) |
                Q(isDone__icontains=search_query)
            )
        self.request.session['filtered_jobs_search'] = search_query
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.session.get('filtered_jobs_search', '')
        return context


# DARBO SUKURIMAS
class JobsCreateView(LoginRequiredMixin, CreateView):
    model = Project_jobs
    form_class = ProjectJobsCreateForm
    template_name = 'Projects/jobs_create.html'
    success_url = reverse_lazy('projects:jobs-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# DARBO ATNAUJINIMAS
class JobsUpdateView(LoginRequiredMixin, UpdateView):
    model = Project_jobs
    form_class = ProjectJobsUpdateForm
    template_name = 'Projects/jobs_update.html'
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    def get_success_url(self):
        if 'last_visited_url' in self.request.session:
            return self.request.session['last_visited_url']
        else:
            return reverse('projects:projects-jobs')

    def get(self, request, *args, **kwargs):
        self.request.session['last_visited_url'] = self.request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)


# DARBO ISTRYNIMAS
@login_required(login_url='/login/')
def JobsDelete(request, pk):
    job = Project_jobs.objects.get(id=pk)
    request.session['last_visited_url'] = request.META.get('HTTP_REFERER')
    job.delete()
    if 'last_visited_url' in request.session:
        return redirect(request.session['last_visited_url'])
    else:
        return redirect('projects:jobs-list')


# SASKAITU LIST'AS
class InvoicesListView(LoginRequiredMixin, ListView):
    model = Invoices
    template_name = 'Projects/invoices_list.html'
    context_object_name = 'invoices'
    login_url = '/login/'
    paginate_by = 10
    ordering = 'invoice_no'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(project_id__project_name__icontains=search_query) |
                Q(status__startswith=search_query)
            )
        self.request.session['filtered_invoices_search'] = search_query
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.session.get('filtered_invoices_search', '')
        return context


# SASKAITOS SUKURIMAS
class InvoicesCreateView(LoginRequiredMixin, CreateView):
    model = Invoices
    form_class = InvoicesCreateForm
    template_name = 'Projects/invoices_create.html'
    success_url = reverse_lazy('projects:invoices-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# SASKAITOS ATNAUJINIMAS
class InvoicesUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoices
    form_class = InvoicesUpdateForm
    template_name = 'Projects/invoices_update.html'
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    def get_success_url(self):
        if 'last_visited_url' in self.request.session:
            return self.request.session['last_visited_url']
        else:
            return reverse('projects:invoices-list')

    def get(self, request, *args, **kwargs):
        self.request.session['last_visited_url'] = self.request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)


# SASKAITOS ISTRYNIMAS
@login_required(login_url='/login/')
def InvoicesDelete(request, pk):
    invoice = Invoices.objects.get(invoice_no=pk)
    request.session['last_visited_url'] = request.META.get('HTTP_REFERER')
    invoice.delete()
    if 'last_visited_url' in request.session:
        return redirect(request.session['last_visited_url'])
    else:
        return redirect('projects:invoices-list')


# SASKAITOS APMOKEJIMO SUKURIMAS
class InvoicePaymentsCreateView(LoginRequiredMixin, CreateView):
    model = Invoice_payments
    form_class = InvoicePaymentsCreateForm
    template_name = 'Projects/invoicePayments_create.html'
    success_url = reverse_lazy('projects:invoices-list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        invoice_no = self.kwargs['invoice_no']
        invoice = get_object_or_404(Invoices, invoice_no=invoice_no)
        form.instance.user = self.request.user
        form.instance.invoice_no = invoice
        return super().form_valid(form)
    

# SASKAITOS APMOKEJIMO ATNAUJINIMAS
class InvoicePaymentsUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice_payments
    form_class = InvoicePaymentsCreateForm
    template_name = 'Projects/invoicePayments_update.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    def get_success_url(self):
        if 'last_visited_url' in self.request.session:
            return self.request.session['last_visited_url']
        else:
            return reverse('projects:invoices-list')

    def get(self, request, *args, **kwargs):
        self.request.session['last_visited_url'] = self.request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)


# SASKAITOS APMOKEJIMO ISTRYNIMAS
@login_required(login_url='/login/')
def InvoicePaymentsDelete(request, pk):
    invoicePayment = Invoice_payments.objects.get(id=pk)
    request.session['last_visited_url'] = request.META.get('HTTP_REFERER')
    invoicePayment.delete()
    if 'last_visited_url' in request.session:
        return redirect(request.session['last_visited_url'])
    else:
        return redirect('projects:invoices-list')


# KONSTRUKCIJU TIPU IR PROJEKTU BUSENU LIST'AS
@login_required(login_url='/login/')
def settings(request):
    constructions = Project_Constructions.objects.filter(user=request.user)
    project_status = Project_Status.objects.filter(user=request.user)
    context = {
        'constructions': constructions,
        'project_status': project_status
    }
    return render(request, 'Projects/settings.html', context)


# KONSTRUKCIJOS TIPO SUKURIMAS
class ConstructionCreateView(LoginRequiredMixin, CreateView):
    model = Project_Constructions
    form_class = ConstructionForm
    template_name = 'Projects/construction_create.html'
    success_url = reverse_lazy('projects:settings')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, 'Toks konstrukcijos tipas jau egzistuoja. Pasirinkite kitą.')
            return self.form_invalid(form)


# KONSTRUKCIJOS TIPO ATNAUJINIMAS
class ConstructionUpdateView(LoginRequiredMixin, UpdateView):
    model = Project_Constructions
    form_class = ConstructionForm
    template_name = 'Projects/construction_create.html'
    success_url = reverse_lazy('projects:settings')
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    

# KONSTRUKCIJOS TIPO ISTRYNIMAS
@login_required(login_url='/login/')
def ConstructionDelete(request, pk):
    construction = Project_Constructions.objects.get(construction_id=pk)
    construction.delete()
    return redirect('projects:settings')


# PROJEKTO BUSENOS SUKURIMAS
class ProjectStatusCreateView(LoginRequiredMixin, CreateView):
    model = Project_Status
    form_class = ProjectStatusForm
    template_name = 'Projects/project_status_create.html'
    success_url = reverse_lazy('projects:settings')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, 'Tokia projekto būsena jau egzistuoja. Pasirinkite kitą.')
            return self.form_invalid(form)


# PROJEKTO BUSENOS ATNAUJINIMAS
class ProjectStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Project_Status
    form_class = ProjectStatusForm
    template_name = 'Projects/project_status_create.html'
    success_url = reverse_lazy('projects:settings')
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, 'Tokia projekto būsena jau egzistuoja. Pasirinkite kitą.')
            return self.form_invalid(form)


# PROJEKTO BUSENOS ISTRYNIMAS
@login_required(login_url='/login/')
def ProjectStatusDelete(request, pk):
    project_status = Project_Status.objects.get(status_id=pk)
    project_status.delete()
    return redirect('projects:settings')
