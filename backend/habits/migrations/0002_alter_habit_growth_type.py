# Generated by Django 4.0.6 on 2022-09-12 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='growth_type',
            field=models.CharField(choices=[('INCREASE', 'INCREASE'), ('DECREASE', 'DECREASE')], max_length=10),
        ),
    ]
