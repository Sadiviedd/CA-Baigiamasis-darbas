from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import timedelta


class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='project id')
    customer_id = models.ForeignKey('Customers', on_delete=models.CASCADE)
    construction_id = models.ForeignKey('Project_Constructions', on_delete=models.SET_NULL, null=True)
    status_id = models.ForeignKey('Project_Status', on_delete=models.SET_NULL, null=True)
    project_name = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    kw = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    modules_w = models.IntegerField(null=True, blank=True)
    eur_kw = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    subcontracting = models.CharField(max_length=150, null=True, blank=True)
    comment = models.CharField(max_length=350, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True, editable=False)
    update_date = models.DateField(auto_now=True, editable=False)

    class Meta:
        db_table = 'Projects'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return self.project_name


class Project_Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=99999)
    status_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='status id')
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Project_Status'
        verbose_name_plural = 'Project_Status'
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_status')
        ]

    def __str__(self):
        return self.name


class Project_Constructions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=99999)
    construction_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='construction id')
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Project_Constructions'
        verbose_name_plural = 'Project_Constructions'
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_construction')
        ]

    def __str__(self):
        return self.name


class Customers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='customer id')
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, null=True, blank=True, unique=True)
    mobile_number = models.IntegerField(null=True, blank=True, unique=True)
    term_days = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Customers'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"{self.name} {self.surname}"


class Project_jobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=99999)
    project_id = models.ForeignKey('Projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_date = models.DateField(default='', null=True, blank=True)
    end_date = models.DateField(default='', null=True, blank=True)
    work_time = models.DecimalField(decimal_places=2, max_digits=10, default= 0, null=True, blank=True)
    break_time = models.DecimalField(decimal_places=2, max_digits=10, default= 0, null=True, blank=True)
    neto_time = models.DecimalField(decimal_places=2, max_digits=10, default=0, editable=False)
    isDone = models.CharField(max_length=5, default="ne", editable=False)

    class Meta:
        db_table = 'Project_jobs'
        verbose_name_plural = 'Project_jobs'
    
    def save(self, *args, **kwargs):
        if self.work_time:
            neto_time = self.work_time - self.break_time
            self.neto_time = round(neto_time, 2)
        if self.end_date:
            self.isDone = "taip"
        else: 
            self.isDone = "ne"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} {self.start_date} {self.end_date} {self.isDone}"


class Invoices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=30, primary_key=True, verbose_name='invoice number')
    project_id = models.ForeignKey('Projects', on_delete=models.CASCADE)
    operation_date = models.DateField(null=True, blank=True)
    deadline_date = models.DateField(default=None, null=True, blank=True)
    term_days = models.IntegerField(default=0)
    amount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    status = models.CharField(max_length=20, editable=False, default='Neapmokėta')
    total_paid = models.DecimalField(default=0, null=True, blank=True, decimal_places=2, max_digits=10)

    class Meta:
        db_table = 'Invoices'
        verbose_name_plural = 'Invoices'

    def save(self, *args, **kwargs):
        if self.operation_date and self.term_days:
            self.deadline_date = self.operation_date + timedelta(days=self.term_days)
        return super(Invoices, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.invoice_no


class Invoice_payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=99999)
    invoice_no = models.ForeignKey('Invoices', related_name='invoice_payments', on_delete=models.CASCADE)
    payment_date = models.DateField()
    paid_amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    class Meta:
        db_table = 'Invoice_payments'
        verbose_name_plural = 'Invoice_payments'
    
    def __str__(self):
        return f"{self.invoice_no} {self.payment_date} {self.paid_amount}"
     

class Project_Expenditures(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey('Projects', on_delete=models.CASCADE)
    operation_date = models.DateField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=150)
    quantity = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    amount = models.DecimalField(decimal_places=2, max_digits=10, editable=False, default=0)

    class Meta:
        db_table = 'Project_Expenditures'
        verbose_name_plural = 'Project_Expenditures'

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


@receiver([post_save, post_delete], sender=Invoice_payments)
def update_invoice_status(sender, instance, **kwargs):
    invoice = instance.invoice_no
    total_payments = invoice.invoice_payments.aggregate(total=models.Sum('paid_amount'))['total'] or 0

    invoice.total_paid = total_payments

    if total_payments >= invoice.amount:
        invoice.status = 'Apmokėta'
    elif total_payments > 0:
        invoice.status = 'Dalinai apmokėta'
    else:
        invoice.status = 'Neapmokėta'

    invoice.save()