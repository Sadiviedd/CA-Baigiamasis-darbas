from django.contrib import admin
from .models import User, Projects, Project_jobs, Invoices, Invoice_payments, Clients


admin.site.register(User)
admin.site.register(Projects)
admin.site.register(Project_jobs)
admin.site.register(Invoices)
admin.site.register(Invoice_payments)
admin.site.register(Clients)