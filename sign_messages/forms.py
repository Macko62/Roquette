from django import forms
from django.db.models.query import FlatValuesListIterable
from django.forms.fields import IntegerField
from .models import mdlSignMessages
from .models import mdlSettings as mSet


class frmSignMessages(forms.ModelForm):

    msgNum=forms.IntegerField(
        label="Message #",
        min_value=1,
        max_value=16)
    tuNumExt=forms.CharField(
        label='Truck #',
        initial='')
    door=forms.CharField(
        label='Door #',
        initial='',
        required=False)
    userOverride=forms.BooleanField(
        label='Override Remote Message',
        initial=False,
        required=False)
    textColor=forms.CharField(
        label='Text Color',
        initial='#ffffff',
        required=False)
    textColorOverride=forms.BooleanField(
        label='Override Global Text Color',
        initial=False,
        required=False
        )
    isFlashing=forms.BooleanField(
        label='Flashing Text',
        initial=False,
        required=False
    )    
    
    class Meta:
        model=mdlSignMessages
        fields=[
            'msgNum',
            'tuNumExt',
            'door',
            'userOverride',
            'textColor',
            'textColorOverride',
            'isFlashing'
        ]

    def clean_data(self,*args,**kwargs):
        _userOverride=False
        if 'userOverride' in self.data: _userOverride=True
        _textColorOverride = False
        if '_textColorOverride' in self.data : _textColorOverride=True
        _isFlashing=FlatValuesListIterable
        if 'isFlashing' in self.data : _isFalshing=True
        ret={
            'msgNum':self.data['msgNum'],
            'tuNumExt':self.data['tuNumExt'],
            'door':self.data['door'],
            'userOverride':_userOverride,
            'textColor':self.data['textColor'],
            'textColorOverride':_textColorOverride,
            'isFlashing':_isFlashing
        }
        return ret


class frmSettings(forms.ModelForm):

    rowsPerPage=forms.IntegerField(
        label="Rows Per Page",
        min_value = 3,
        max_value=5
    )
    scrollSpeed=forms.IntegerField(
        label='Scroll Speed',
        min_value=1,
        max_value=60
    )
    flashPeriod=forms.FloatField(
        label="Flashing Period",
        min_value=0.5,
        max_value=3.0
    )
    pageDwell=forms.IntegerField(
        label='Page Dwell',
        max_value=3598
    )
    ipAddress=forms.CharField(
        label='Remote Data IP',
        required=False,
        initial=''
    )
    bgColor=forms.CharField(
        label='Background Color',
        required=False
    )
    textColor=forms.CharField(
        label='Text Color',
        required=False
    )
    testMode=forms.BooleanField(
        label='Pixel Test Mode',
        required=False
    )
    
    class Meta:
        model = mSet
        fields=[
            'rowsPerPage',
            'scrollSpeed',
            'flashPeriod',
            'pageDwell',
            'ipAddress',
            'bgColor',
            'textColor',
            'testMode'
        ]
    
    def clean_data(self,*args,**kwargs):
        myBool = False
        if 'testMode' in self.data: myBool = True
        return {
            'rowsPerPage':self.data['rowsPerPage'],
            'scrollSpeed':self.data['scrollSpeed'],
            'flashPeriod':self.data['flashPeriod'],
            'pageDwell':self.data['pageDwell'],
            'ipAddress':self.data['ipAddress'],
            'bgColor':self.data['bgColor'],
            'textColor':self.data['textColor'],
            'testMode':myBool
        }