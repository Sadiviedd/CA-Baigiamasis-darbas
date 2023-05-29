from django.contrib import admin
from .models import Projects, Project_jobs, Invoices, Invoice_payments, Project_Expenditures , Customers, Project_Status, Project_Constructions


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'customer_name', 'construction_name', 'status_name', 'address', 'kw', 'modules_w', 'eur_kw', 'subcontracting', 'create_date', 'update_date')

    def customer_name(self, obj):
        return obj.customer_id.name
    
    def construction_name(self, obj):
        return obj.construction_id.name

    def status_name(self, obj):
        return obj.status_id.name


class InvoicesAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'invoice_no', 'operation_date', 'deadline_date', 'amount', 'status')

    def project_name(self, obj):
        return obj.project_id.project_name


class Invoice_PaymentsAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'invoice_no', 'payment_date', 'paid_amount')

    def project_name(self, obj):
        return obj.invoice_no.project_id.project_name


class Project_ExpendituresAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'operation_date', 'name', 'quantity', 'price', 'amount')

    def project_name(self, obj):
        return obj.project_id.project_name


class Project_jobsAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'title', 'start_date', 'end_date', 'break_time', 'neto_time', 'isDone')

    def project_name(self, obj):
        return obj.project_id.project_name


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'mobile_number', 'term_days')


class Project_ConstructionsAdmin(admin.ModelAdmin):
    list_display = ('construction_id', 'name')


class Project_StatusAdmin(admin.ModelAdmin):
    list_display = ('status_id', 'name')


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Project_jobs, Project_jobsAdmin)
admin.site.register(Invoices, InvoicesAdmin)
admin.site.register(Invoice_payments, Invoice_PaymentsAdmin)
admin.site.register(Project_Expenditures, Project_ExpendituresAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Project_Status, Project_StatusAdmin)
admin.site.register(Project_Constructions, Project_ConstructionsAdmin)