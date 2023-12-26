# Generated by Django 4.1.7 on 2023-05-29 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0009_alter_bill_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='cusid',
            field=models.ForeignKey(blank=True, db_column='CUSID', null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.customer'),
        ),
    ]
