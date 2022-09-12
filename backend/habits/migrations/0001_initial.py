# Generated by Django 4.0.6 on 2022-09-11 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('estimate_type', models.CharField(choices=[('TIME', 'TIME'), ('COUNT', 'COUNT')], max_length=10)),
                ('estimate_unit', models.CharField(max_length=10)),
                ('final_goal', models.PositiveIntegerField()),
                ('growth_type', models.CharField(choices=[('INC', 'INCREASE'), ('DEC', 'DECREASE')], max_length=10)),
                ('day_cycle', models.PositiveSmallIntegerField(default=0)),
                ('today_goal', models.PositiveIntegerField()),
                ('today_progress', models.PositiveIntegerField()),
                ('growth_amount', models.IntegerField()),
                ('last_done_date', models.DateTimeField(blank=True)),
                ('is_running', models.BooleanField(default=False)),
                ('is_paused', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(blank=True)),
                ('paused_date', models.DateTimeField(blank=True)),
                ('temporary_progress', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RoundRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('progress', models.PositiveIntegerField()),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.habit')),
            ],
        ),
        migrations.CreateModel(
            name='DailyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('goal', models.PositiveIntegerField()),
                ('progress', models.PositiveIntegerField()),
                ('success', models.BooleanField()),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.habit')),
            ],
        ),
    ]