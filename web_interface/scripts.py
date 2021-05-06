from tkinter import * 
from pathlib import Path
import requests
import json

class table():

    def __init__(self):
        # list holding data base rows
        self.data=[]
        # list of column widths
        self.colWidths=[10,4]
        # list holding window label widgets
        self.labels=[]
        # count of database rows
        self.lenData=len(self.data)
        # count of label widgets
        self.lenLabels=len(self.labels)
        # update interval
        self.interval=60_000
        # root path, not currently used
        self.rootDir=Path(__file__).resolve().parent.parent
        # url of remote data
        self.urlRemote='http://192.168.0.200:8000/'
        # url of local data
        self.urlGetLocal='http://127.0.0.1:8000/get/'
        # url to store data to database
        self.urlPutLocal='http://127.0.0.1:8000/put/'
        # tkinter window object
        self.w=Tk()
        # tkinter window object attribute presets
        self.w.attributes('-topmost',True)#('-fullscreen',True,'-topmost',True)
        self.w.overrideredirect(True) 
        # set tkinter window object background to black
        self.w.configure(bg='black',bd='-2')
        # escape key exits application
        self.w.bind('<Escape>',lambda x: self.w.destroy())

    def addHeader(self): # draws static header for table columns
        self.addHeaderElement('TRUCK',self.colWidths[0])
        self.addHeaderElement('DOOR',self.colWidths[1])

    def addHeaderElement(self,label,width): # add specified text to header row
        self.labels.append(Label(
            self.w,
            bg='black',
            fg='white',
            font='consolas 12 bold',
            text=label,
            width=width,
            height=1
        ))
        self.lenLabels=len(self.labels)
        self.labels[self.lenLabels-1].grid(row=0,column=self.lenLabels-1)

    def getCSpan(self,r,c):
        if c==0 and self.data[r]['door'] == '': return 2
        return 1

    def addLabel(self): # adds rows to dynamic portion of table; skips blank rows
        for r in range(0,self.lenData):
            for c in range(0,2):
                lblText=self.getLabelText(r,c)
                if lblText!='null' and lblText!='':
                    self.labels.append(
                        Label(
                            self.w,
                            bg='black',
                            fg='white',
                            font='consolas 12 bold',
                            text=lblText,
                            width=self.getColumnWidth(r,c),
                            height=1
                        )
                    )
                    self.lenLabels=len(self.labels)
                    self.labels[self.lenLabels-1].grid(
                        row=r+1,
                        column=c,
                        columnspan=self.getCSpan(r,c)
                    )

    def getColumnWidth(self,r,c): # lookup table for column widths
        if self.getCSpan(r,c)==2: return sum(self.colWidths)
        else: return self.colWidths[c]

    def getData(self,url): # gets data for processing
        x=requests.get(url)
        data=x.json()
        return data

    def getLabelText(self,row,column): # get local data for table
            if column==0: return self.data[row]['tuNumExt']
            if column==1: return self.data[row]['door']

    def fillRemoteData(self,data): # 2add missing dictionary fields to remote data
        for i,e in enumerate(data):
            e['msgNum']=i+1
            e['userOverride']=False
    
    def updateData(self): # process local and remote data for display and storage in database
        #rmData=self.getData(self.urlRemote)
        f = open('C:\\Users\\Roquette\\Desktop\\interface\\src\\web_interface\\messages.json')
        rmData=json.load(f)
        self.fillRemoteData(rmData)
        lclData=self.getData(self.urlGetLocal)
        rmDataR=len(rmData)
        for i,local in enumerate(lclData):
            if not local['userOverride']:
                if i<rmDataR:
                    lclData[i]=rmData[i]
                if i>=rmDataR:
                    lclData[i]['tuNumExt']='null'
                    lclData[i]['door']='null'
        self.data=lclData
        self.lenData=len(self.data)

    def putData(self): # save local data to database
        for r in self.data:
            x=requests.put(self.urlPutLocal,r)
            delta=0
            while x.status_code!=201:
                delta+=1
                print(x.status_code)
                print(delta)
                if delta>=500: break

    def getWidgets(self): # returns a list of tkinter window child widgets
        ret=self.w.winfo_children()
        for i in ret:
            if i.winfo_children():ret.extend(i.winfo_children())
        return ret

    def clearChildren(self): # removes tkinter window child widgets
        for c in self.getWidgets():
            c.destroy()

    def clearGrid(self): # removes tkinter window grid child objects
        for l in self.w.grid_slaves(): 
            l.grid_forget()
            l.destroy()

    def updateTable(self): # process remote and local data; draw table to window
        # destroy tkinter window grid objects
        self.clearGrid()
        # destroy tkinter window child objects        
        self.clearChildren()
        # clear label list  
        self.labels=[]
        # clear data list          
        self.data=[]
        # add static labels for table
        self.addHeader()
        # process local and remote data, save to local data
        self.updateData()       
        # save local data to database
        self.putData()
        # build dynamic portion of table
        self.addLabel()
        # update table cyclically
        self.w.after(self.interval,self.updateTable)

t=table()
t.updateTable()
t.w.mainloop()   