# Generated by Django 4.1.7 on 2023-03-04 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0002_account_balance_alter_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]