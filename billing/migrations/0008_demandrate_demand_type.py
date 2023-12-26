# Generated by Django 4.1.7 on 2023-05-29 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_alter_demandrate_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandrate',
            name='demand_type',
            field=models.ForeignKey(blank=True, db_column='Demand_Type_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='billing.demandtype'),
        ),
    ]