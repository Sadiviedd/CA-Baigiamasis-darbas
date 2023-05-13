# Generated by Django 4.2.1 on 2023-05-06 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0002_alter_clients_options_alter_invoice_payments_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='status',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='projects',
            name='construction_type',
            field=models.CharField(choices=[('Ploksčias bituminis', 'Ploksčias bituminis'), ('Antžeminė', 'Antžeminė'), ('Classic valcuota skarda', 'Classic valcuota skarda'), ('Trapecinė skarda', 'Trapecinė skarda'), ('Čerpinė skarda', 'Čerpinė skarda'), ('Šiferis', 'Šiferis'), ('Molinė čerpė', 'Molinė čerpė'), ('Šlaitinė', 'Šlaitinė'), ('Betoninė čerpė', 'Betoninė čerpė'), ('Bituminė čerpė', 'Bituminė čerpė')], default=None, max_length=100),
        ),
    ]