# Generated by Django 2.2 on 2019-05-04 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('name', models.CharField(db_index=True, max_length=191)),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='risk_types', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('client', models.CharField(db_index=True, max_length=191)),
                ('risk_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risks', to='core.RiskType')),
            ],
            options={
                'ordering': ['client'],
            },
        ),
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('currency', 'Currency'), ('date', 'Date'), ('enum', 'Enum'), ('number', 'Number'), ('text', 'Text')], max_length=19)),
                ('name', models.CharField(db_index=True, max_length=191)),
                ('options', models.CharField(max_length=1024, null=True)),
                ('required', models.BooleanField(default=True)),
                ('risk_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_types', to='core.RiskType')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=191)),
                ('field_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='core.FieldType')),
                ('risk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='core.Risk')),
            ],
            options={
                'ordering': ['risk', 'field_type'],
            },
        ),
    ]
