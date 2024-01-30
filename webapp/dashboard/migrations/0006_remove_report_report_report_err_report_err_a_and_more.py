# Generated by Django 4.0.2 on 2024-01-30 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_rename_report_report_report_urltable_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='report',
        ),
        migrations.AddField(
            model_name='report',
            name='err',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='err_A',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='err_AA',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='err_AAA',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='likely',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='num_A',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='num_AA',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='num_AAA',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='num_err',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='num_likely',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='num_potential',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='potential',
            field=models.JSONField(blank=True, null=True),
        ),
    ]