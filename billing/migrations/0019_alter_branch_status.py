# Generated by Django 4.1.7 on 2023-07-10 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0018_rename_payment_paymentcus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Due', 'Due')], db_column='Status', max_length=200, null=True),
        ),
    ]
