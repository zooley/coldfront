# Generated by Django 2.0.6 on 2018-07-30 22:05

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('project_number', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(255)], verbose_name='Project Number from funding agency')),
                ('title', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(255)])),
                ('role', models.CharField(choices=[('PI', 'Principal Investigator (PI)'), ('CoPI', 'Co-Principal Investigator (CoPI)'), ('SP', 'Senior Personnel (SP)')], default='PI', max_length=10)),
                ('pi_full_name', models.CharField(blank=True, max_length=255)),
                ('other_funding_agency', models.CharField(blank=True, max_length=255)),
                ('rf_award_number', models.PositiveIntegerField(blank=True)),
                ('project_start', models.DateField(verbose_name='Project Start Date')),
                ('project_end', models.DateField(verbose_name='Project End Date')),
                ('percent_credit', models.FloatField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('direct_funding', models.FloatField()),
                ('total_amount_awarded', models.FloatField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Archived', 'Archived')], default='Active', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Grants',
            },
        ),
        migrations.CreateModel(
            name='GrantFundingAgency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='grant',
            name='funding_agency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grant.GrantFundingAgency'),
        ),
        migrations.AddField(
            model_name='grant',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
    ]
