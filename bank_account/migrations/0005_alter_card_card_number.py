# Generated by Django 4.1.7 on 2023-03-04 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0004_alter_card_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_number',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
