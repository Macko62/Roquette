# Generated by Django 3.1.4 on 2021-02-24 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_messages', '0010_auto_20210224_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='mdlsettings',
            name='textColor',
            field=models.TextField(default='#000000'),
        ),
    ]
