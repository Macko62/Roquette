from django.contrib import admin
from .models import (
    mdlSignMessages,
    mdlSettings as mSet
)
# Register your models here.
admin.site.register(mdlSignMessages)
admin.site.register(mSet)