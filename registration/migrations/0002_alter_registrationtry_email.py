# Generated by Django 4.1.2 on 2022-10-17 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationtry',
            name='email',
            field=models.EmailField(db_index=True, error_messages={'unique': 'Not a valid email. Enter again and correctly.'}, max_length=254, unique=True),
        ),
    ]
