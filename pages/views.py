from json import dumps,loads
from django.shortcuts import render
from sign_messages.serializers import smSerializer
from django.core import serializers
from sign_messages.models import mdlSignMessages
from sign_messages.forms import frmSignMessages
from sign_messages.scripts import writeMsgs
from sign_messages.models import mdlSettings as mSet
from sign_messages.forms import frmSettings as fSet
from sign_messages.scripts import writeSettings
from datetime import datetime as dt
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

#Authenication
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index_view(request,*args,**kwargs):
    if request.method =='POST':
        writeMsgs(request)
    form=frmSignMessages()
    object_list=mdlSignMessages.objects.all()
    objCount=len(object_list)
    dispPointerList=[x for x in range(objCount)]
    settings=processedSettings(mSet.objects.first())
    as_json=dumps(processObjList(getObjList(objCount,object_list,dispPointerList)))
    context = {
        'object_list':object_list,
        'settings':settings,
        'form':form,
        'as_json':as_json
    }
    return render(request,'editMessages.html',context)

@login_required(login_url='login')
def settings_view(request,*args,**kwargs):
    updated=False
    if request.method =='POST':
        updated=writeSettings(request)
    form=fSet(instance=mSet.objects.first())
    context={
        'form':form,
        'updated':updated
    }
    return render(request,'settings.html',context)


def calc_delta(now, then):
    now_converted = 60*now[0]+now[1]
    then_converted = 60*then[0]+then[1]
    ret = now_converted - then_converted
    if ret < 0:
        ret += 3600
    return ret


def trgrNextPage(request):
    pageDwell=mSet.objects.first().pageDwell
    now=[dt.now().minute, dt.now().second]
    then=request.session.get('lastPageChange')
    delta=calc_delta(now, then)
    if delta>=pageDwell:
        request.session['lastPageChange']=[
            dt.now().minute, 
            dt.now().second
        ]
        return True


def initSessionVars(request,rowsPerPage):
    if request.session.get('lastPageChange') is None:
        request.session['lastPageChange']=[
            dt.now().minute, 
            dt.now().second
        ]
    dispList=request.session.get('dispList')
    if dispList is None or len(dispList)!=rowsPerPage: 
        l=[x for x in range(rowsPerPage)]
        request.session['dispList']=l 
    if request.session.get('noConnCounter') is None:
        request.session['noConnCounter']=0


def updateDispPointerList(request,rowsPerPage,objList):
    dispList=request.session.get('dispList')
    firstRow=dispList[-1]+1
    memScanner=0
    totalRows=len(objList)
    for pDisp in range(rowsPerPage):
        pObj=pDisp+firstRow+memScanner
        if pObj>totalRows: pObj=pObj-totalRows
        while (objList[pObj].tuNumExt=='null'):
            memScanner+=1
            pObj+=1
            if pObj>=totalRows:pObj-=totalRows
        dispList[pDisp]=pObj
    request.session['dispList']=dispList
    return dispList


def getObjList(rowsPerPage,objList,dispPointerList):
    dispObjList=[x for x in range(rowsPerPage)]
    for pRow in range(rowsPerPage):
        dispObjList[pRow]=objList[dispPointerList[pRow]]
    return dispObjList


def dispObjToDict(dispObj):
    ret={
        'msgNum' : dispObj.msgNum,
        'tuNumExt' : dispObj.tuNumExt,
        'door' : dispObj.door,
        'userOverride' : dispObj.userOverride,
        'textColor' : dispObj.textColor,
        'textColorOverride' : dispObj.textColorOverride,
        'isFlashing' : dispObj.isFlashing
    }
    return ret


def processObjList(dispObjList):
    ret = []
    for dispObj in dispObjList: 
        ret.append(dispObjToDict(dispObj))
    return ret


def processedSettings(settings):
    ret={
        'rowsPerPage':settings.rowsPerPage,
        'scrollSpeed':settings.scrollSpeed,
        'pageDwell':settings.pageDwell,
        'flashPeriod':settings.flashPeriod,
        'ipAddress':settings.ipAddress,
        'bgColor':settings.bgColor,
        'textColor':settings.textColor,
        'testMode':settings.testMode,
        'browserRefresh':int(settings.pageDwell/2),
        'fontSize':0,
        'rowHeight':0,
        'c0Width':0,
        'c1Width':0
    }
    ret['fontSize']=11+(5-ret['rowsPerPage'])*2
    ret['rowHeight']=11+(5-ret['rowsPerPage'])*2
    if ret['rowsPerPage']==3:
        ret['c0Width']=67
        ret['c1Width']=43
    if ret['rowsPerPage']==4:
        ret['c0Width']=60
        ret['c1Width']=40
    if ret['rowsPerPage']==5:
        ret['c0Width']=55
        ret['c1Width']=45
    return ret


def getData(url):
    s=requests.Session()
    s.auth=('DISP294','S8z~v*Sxp!D6Zf:D')
    # s.cert=('c:/Apache24/conf/Roquette_inter_full.cer')
    r=s.get(url).text
    soup=BeautifulSoup(r,"lxml")
    data=loads(soup.pre.text)
    return data


def writeData(data, objList):
    p_data=0
    for x in objList:
        if p_data < len(data):
            if not x.userOverride:
                x.tuNumExt = data[p_data]['tuNumExt']
                x.door = data[p_data]['door']
                x.save()
            p_data+=1


def checkComm(dispObjList, noConnCounter):
    if noConnCounter >= 10:
        for o in dispObjList:
            if not o['userOverride']:
                o['tuNumExt'] = 'no comm'
                o['door'] = ''


def logError(error, logFile):
    f = open(logFile, 'a')
    f.write(str(dt.now()) + '; ' + str(error) + '\n')
    f.close()
    if os.path.getsize(logFile) > 10_000_000:
        os.remove(logFile)


def sign(request,*args,**kwargs):
    rowsPerPage=mSet.objects.first().rowsPerPage
    initSessionVars(request,rowsPerPage)
    objList=mdlSignMessages.objects.all()
    if trgrNextPage(request): 
        dispPointerList=updateDispPointerList(request,rowsPerPage,objList)
    else: 
        dispPointerList=request.session.get('dispList')
    dispObjList=processObjList(getObjList(rowsPerPage,objList,dispPointerList))
    settings=processedSettings(mSet.objects.first())
    checkComm(dispObjList, request.session['noConnCounter'])
    as_json={
        'objects':dispObjList,
        'settings':settings
    }
    context = {
        'settings':settings,
        'objects':dispObjList,
        'as_json':dumps(as_json)
    }
    try:
        #data=getData(settings['ipAddress'])
        data = getData('http://159.89.182.128')
        request.session['noConnCounter']=0
        writeData(data, objList)
    except Exception as e:
        logError(e, 'error_log.txt')
        print (e)
        request.session['noConnCounter']+=1
    return render(request,'signContent.html',context)