from django.urls import path
from .views import (
    project_detail_view,
    ProjectsListView,
    ProjectCreateView,
    ProjectsUpdateView,
    ProjectsDelete,
    JobsListView,
    JobsCreateView,
    JobsUpdateView,
    JobsDelete,
    CustomersListView,
    CustomersCreateView,
    CustomersUpdateView,
    CustomerDelete,
    ExpendituresListView,
    ExpendituresCreateView,
    ExpendituresUpdateView,
    ExpendituresDelete,
    InvoicesListView,
    InvoicesCreateView,
    InvoicesUpdateView,
    InvoicesDelete,
    InvoicePaymentsCreateView,
    InvoicePaymentsUpdateView,
    InvoicePaymentsDelete,
    settings,
    ConstructionCreateView,
    ConstructionUpdateView,
    ConstructionDelete,
    ProjectStatusCreateView,
    ProjectStatusUpdateView,
    ProjectStatusDelete,
)

app_name = 'Projects'

urlpatterns = [
    path('', ProjectsListView.as_view(), name='projects-list'),
    path('create/', ProjectCreateView.as_view(), name='projects-create'),
    path('update/<int:pk>/', ProjectsUpdateView.as_view(), name='projects-update'),
    path('delete/<int:pk>/', ProjectsDelete, name='projects-delete'),
    path('projectDetail/<int:pk>/', project_detail_view, name='projects-detail'),
    path('jobs/', JobsListView.as_view(), name='jobs-list'),
    path('jobs/create/', JobsCreateView.as_view(), name='jobs-create'),
    path('jobs/update/<int:pk>/', JobsUpdateView.as_view(), name='jobs-update'),
    path('jobs/delete/<int:pk>/', JobsDelete, name='jobs-delete'),
    path('customers/', CustomersListView.as_view(), name='customers-list'),
    path('customers/create/', CustomersCreateView.as_view(), name='customers-create'),
    path('customers/update/<int:pk>/', CustomersUpdateView.as_view(), name='customers-update'),
    path('customers/delete/<int:pk>/', CustomerDelete, name='customers-delete'),
    path('expenditures/', ExpendituresListView.as_view(), name='expenditures-list'),
    path('expenditures/create/', ExpendituresCreateView.as_view(), name='expenditures-create'),
    path('expenditures/update/<int:pk>/', ExpendituresUpdateView.as_view(), name='expenditures-update'),
    path('expenditures/delete/<int:pk>/', ExpendituresDelete, name='expenditures-delete'),
    path('invoices/', InvoicesListView.as_view(), name='invoices-list'),
    path('invoices/create/', InvoicesCreateView.as_view(), name='invoices-create'),
    path('invoices/update/<str:pk>/', InvoicesUpdateView.as_view(), name='invoices-update'),
    path('invoices/delete/<str:pk>/', InvoicesDelete, name='invoices-delete'),
    path('invoices/invoicePayments/create/<str:invoice_no>/', InvoicePaymentsCreateView.as_view(), name='invoicePayments-create'),
    path('invoices/invoicePayments/update/<int:pk>/', InvoicePaymentsUpdateView.as_view(), name='invoicePayments-update'),
    path('invoices/invoicePayments/delete/<int:pk>/', InvoicePaymentsDelete, name='invoicePayments-delete'),
    path('settings/', settings, name='settings'),
    path('settings/construction/create/', ConstructionCreateView.as_view(), name='construction-create'),
    path('settings/construction/update/<int:pk>/', ConstructionUpdateView.as_view(), name='construction-update'),
    path('settings/construction/delete/<int:pk>/', ConstructionDelete, name='construction-delete'),
    path('settings/project_status/create/', ProjectStatusCreateView.as_view(), name='project-status-create'),
    path('settings/project_status/update/<int:pk>/', ProjectStatusUpdateView.as_view(), name='project-status-update'),
    path('settings/project_status/delete/<int:pk>/', ProjectStatusDelete, name='project-status-delete'),
]