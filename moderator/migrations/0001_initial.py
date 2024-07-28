# Generated by Django 5.0.7 on 2024-07-19 17:09

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import moderator.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('contact', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Donar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=50)),
                ('thana', models.CharField(max_length=50)),
                ('blood_group', models.CharField(choices=[('1', 'A+'), ('2', 'A-'), ('3', 'B+'), ('4', 'B-'), ('5', 'AB-'), ('6', 'AB-'), ('7', 'O+'), ('8', 'O-')], max_length=10)),
                ('last_donate', models.DateField()),
                ('contact_number', models.IntegerField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donor_acount', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=200)),
                ('establishing_year', models.IntegerField()),
                ('logo', models.ImageField(null=True, upload_to=moderator.models.moderatorImgUpload)),
                ('organization_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]