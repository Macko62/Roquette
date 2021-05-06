# Generated by Django 3.1.4 on 2021-02-25 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_messages', '0012_auto_20210225_0419'),
    ]

    operations = [
        migrations.AddField(
            model_name='mdlsignmessages',
            name='isFlashing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mdlsignmessages',
            name='textColor',
            field=models.TextField(default='#ffffff'),
        ),
        migrations.AddField(
            model_name='mdlsignmessages',
            name='textColorOverride',
            field=models.BooleanField(default=False),
        ),
    ]