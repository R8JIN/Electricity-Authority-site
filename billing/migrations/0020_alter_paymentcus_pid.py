# Generated by Django 4.1.7 on 2023-07-10 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0019_alter_branch_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentcus',
            name='pid',
            field=models.AutoField(db_column='PID', primary_key=True, serialize=False),
        ),
    ]
