# Generated migration to add phone_number and address fields

from django.db import migrations, models
import accounts.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[accounts.validators.validate_phone_number]),
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, validators=[accounts.validators.validate_safe_text]),
        ),
        migrations.AddField(
            model_name='user',
            name='membership_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_active_member',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('member', 'Library Member'),
                    ('librarian', 'Librarian'),
                    ('admin', 'Administrator'),
                    ('student', 'Student'),
                    ('lecturer', 'Lecturer'),
                ],
                default='member',
                max_length=20
            ),
        ),
    ]