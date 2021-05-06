from sign_messages.models import mdlSignMessages
from sign_messages.forms import frmSignMessages
from sign_messages.models import mdlSettings as mSet
from sign_messages.forms import frmSettings as fSet

def writeMsgs(request):
    print(request.POST)
    msgNum=int(request.POST['msgNum'])+int(mdlSignMessages.objects.first().id)-1
    try:
        obj=mdlSignMessages.objects.get(id=msgNum)
        form=frmSignMessages(request.POST,instance=obj)
        if form.is_valid(): form.save()
    except:
        form=frmSignMessages(request.POST)
        obj=mdlSignMessages.objects.create(**form.clean_data())

def writeSettings(request):
    try:
        obj=mSet.objects.first()
        form=fSet(request.POST,instance=obj)
        if form.is_valid(): form.save()
    except:
        form=fSet(request.POST)
        obj=mSet.objects.create(**form.clean_data())
    return True