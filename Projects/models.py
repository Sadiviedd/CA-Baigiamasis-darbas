from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass


class Projects(models.Model):
    CONSTRUCTION_TYPE_CHOICES = [
        ('Ploksčias bituminis', 'Ploksčias bituminis'),
        ('Antžeminė', 'Antžeminė'),
        ('Classic valcuota skarda', 'Classic valcuota skarda'),
        ('Trapecinė skarda', 'Trapecinė skarda'),
        ('Čerpinė skarda', 'Čerpinė skarda'),
        ('Šiferis', 'Šiferis'),
        ('Molinė čerpė', 'Molinė čerpė'),
        ('Šlaitinė', 'Šlaitinė'),
        ('Betoninė čerpė', 'Betoninė čerpė'),
        ('Bituminė čerpė', 'Bituminė čerpė'),
    ]
    STATUS_CHOICES = [
        ('Gautas kontaktas iš Saulės grąžos', 'Gautas kontaktas iš Saulės grąžos'),
        ('LDA kontraktas', 'LDA kontraktas'),
        ('Susisiekta', 'Susisiekta'),
        ('Aplankyta', 'Aplankyta'),
        ('Išsiųstas pasiūlymas', 'Išsiųstas pasiūlymas'),
        ('Pasiektas susitarimas', 'Pasiektas susitarimas'),
        ('Pasirašyta sutartis', 'Pasirašyta sutartis'),
        ('Projektas įgyvendintas', 'Projektas įgyvendintas'),
        ('Rangovo deklaracija', 'Rangovo deklaracija'),
        ('Perduota subrangai', 'Perduota subrangai'),
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    client_id = models.ForeignKey('Clients', on_delete=models.PROTECT)
    address = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    construction_type = models.CharField(max_length=100, choices=CONSTRUCTION_TYPE_CHOICES, default='')
    kw = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    eur_kw = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    modules_w = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='')
    subcontracting = models.CharField(max_length=200, null=True, blank=True)
    comment = models.CharField(max_length=350, null=True, blank=True)
    update_date = models.DateField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Projects'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return f"{self.client_id} {self.address} {self.city} {self.kw} {self.eur_kw} {self.modules_w}"


class Clients(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True, unique=True)
    mobile_number = models.IntegerField(null=True, blank=True, unique=True)
    term_days = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Clients'
        verbose_name_plural = 'Clients'
    
    def __str__(self):
        return f"{self.name} {self.surname}"


class Project_jobs(models.Model):
    project_id = models.ForeignKey('Projects', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    start_date = models.DateField(default='', null=True, blank=True)
    end_date = models.DateField(default='', null=True, blank=True)
    done = models.BooleanField(default=False)
    time = models.DurationField(null=True, blank=True, default='00:00:00')

    class Meta:
        db_table = 'Project_jobs'
        verbose_name_plural = 'Project_jobs'

    # is_done funckija atsakinga uz darbo atlikimo statusa.
    # jeigu darbas atliktas, vartotojas pazymi, kad atliktas.
    def is_done(self):
        self.done = True
        self.save()
    
    def __str__(self):
        return f"{self.title} {self.start_date} {self.end_date} {self.done} {self.time}"


class Invoices(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    invoice_no = models.CharField(max_length=30, primary_key=True)
    project_id = models.ForeignKey('Projects', on_delete=models.PROTECT)
    deadline_date = models.DateField(default='', null=True, blank=True)
    amount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    status = models.CharField(max_length=20, editable=False, default='Neapmokėta')

    class Meta:
        db_table = 'Invoices'
        verbose_name_plural = 'Invoices'

    
    def __str__(self):
        return f"{self.invoice_no} {self.deadline_date} {self.amount} {self.status}"


class Invoice_payments(models.Model):
    invoice_no = models.ForeignKey('Invoices', related_name='invoice_payments', on_delete=models.PROTECT)
    payment_date = models.DateField(default='', null=True, blank=True)
    paid_amount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)

    class Meta:
        db_table = 'Invoice_payments'
        verbose_name_plural = 'Invoice_payments'
    
    def __str__(self):
        return f"{self.invoice_no} {self.payment_date} {self.paid_amount}"
    

@receiver(post_save, sender=Invoice_payments)
def update_invoice_status(sender, instance, **kwargs):
    invoice = instance.invoice_no
    total_payments = invoice.invoice_payments.aggregate(total=models.Sum('paid_amount'))['total'] or 0
    if total_payments == invoice.amount:
        invoice.status = 'Apmokėta'
    elif total_payments > 0:
        invoice.status = 'Dalinai apmokėta'
    else:
        invoice.status = 'Neapmokėta'
    invoice.save()