# Generated by Django 3.1.4 on 2021-02-25 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_messages', '0011_mdlsettings_textcolor'),
    ]

    operations = [
        migrations.AddField(
            model_name='mdlsettings',
            name='testMode',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mdlsettings',
            name='textColor',
            field=models.TextField(default='#ffffff'),
        ),
    ]
