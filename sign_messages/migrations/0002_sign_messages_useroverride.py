# Generated by Django 3.1.4 on 2020-12-28 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sign_messages',
            name='userOverride',
            field=models.BooleanField(default=False),
        ),
    ]