# Generated by Django 4.1.2 on 2023-01-18 09:25

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('estimate_type', models.CharField(choices=[('TIME', 'TIME'), ('COUNT', 'COUNT')], max_length=10)),
                ('estimate_unit', models.CharField(blank=True, max_length=10)),
                ('final_goal', models.PositiveIntegerField()),
                ('growth_type', models.CharField(choices=[('INCREASE', 'INCREASE'), ('DECREASE', 'DECREASE')], max_length=10)),
                ('day_cycle', models.PositiveSmallIntegerField(default=0)),
                ('importance', models.PositiveSmallIntegerField(default=100, validators=[django.core.validators.MaxValueValidator(10000)])),
                ('level', models.PositiveIntegerField(default=1)),
                ('goal_xp', models.PositiveIntegerField(default=0)),
                ('current_xp', models.PositiveIntegerField(default=0)),
                ('growth_amount', models.IntegerField(default=0)),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('is_today_due_date', models.BooleanField(default=True)),
                ('is_done', models.BooleanField(default=False)),
                ('is_running', models.BooleanField(default=False)),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('is_paused', models.BooleanField(default=False)),
                ('paused_datetime', models.DateTimeField(blank=True, null=True)),
                ('temporary_progress', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoundRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('progress', models.PositiveIntegerField()),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.habit')),
            ],
        ),
        migrations.CreateModel(
            name='DailyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('success', models.BooleanField()),
                ('level_now', models.PositiveIntegerField()),
                ('level_change', models.IntegerField()),
                ('xp_change', models.IntegerField()),
                ('xp_accumulate', models.PositiveIntegerField()),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.habit')),
            ],
        ),
    ]
