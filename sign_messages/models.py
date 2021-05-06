from django.db import models

# Create your models here.
class mdlSignMessages(models.Model):
    msgNum=models.IntegerField(default=-1)
    tuNumExt=models.TextField(default='')
    door=models.TextField(default='',blank=True)
    userOverride=models.BooleanField(default=False)
    textColor=models.TextField(default='#ffffff')
    textColorOverride=models.BooleanField(default=False)
    isFlashing=models.BooleanField(default=False)

class mdlSettings(models.Model):
    rowsPerPage=models.IntegerField(default=5)
    scrollSpeed=models.IntegerField(default=3)
    pageDwell=models.IntegerField(default=10)
    ipAddress=models.TextField(default='')
    bgColor=models.TextField(default='#000000')
    textColor=models.TextField(default='#ffffff')
    testMode=models.BooleanField(default=False)
    flashPeriod=models.FloatField(default=1.5)