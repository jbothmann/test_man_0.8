from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkSelectLabel import * #Local Import
from datetime import datetime
from struct import *
from time import sleep

import serial
import types
import json
import copy
import os
import string
import random

version = "0.8"

main_url = "http://127.0.0.1:5000/"

numberOfData = 32
numberOfControls = 32

#base64 encoded bytestring which contains the favicon
encoded_string = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASQSURBVHhe7ZpdbBRVFMf/K61AgFKxfegmoA9SC0E0JGCIBqg0giH6Ag+KL2BEjU3E+PEkbJAHNDHVaAL4EYUH06A+iAFMSSG8WROFAm2wHyDGpppAhLZJW+luOZ7LnAnb7el054tpnPml/5x77+69e8+ZO/djpikC+C++3CU2tiQBEBtbkgCIjS1JAMTGliQAYmNLEgCxsSUJgNjYcmdOg6WlwPp1wIYNQHU1h32afMA/ffOmpBmTtntDJp3XtdFRSTCm3P7M2MI2bG61l/e9N94EenqsvI00FZ7q1hJ1dhCN5qLV0SNq/8IdAS+9COzdx1c84jstmwWWLQMu/CYFtwmvZ2tWTw3nDQcPqM4bwhkBd/M939oK1NRIQYQMDAAPcj+uXJGCsYRzebZtmxrOGxoaJnTeEPwImDcP6OywbNT09loXYmhYCsYT/AjI7Jgazht2vOPovCHYEWDW+PPnrHXfiWPHLOVyUhAQ5eXAqlW851gPtJ0Hlj/K3k3inglAYPrhe30NzlfbOaLp0/X6QenhpUQrV+qfFSi4ADxRqzucr6FBq3Na/YgUTABKSohaz+hO5+v17Xr9CBVMALZu0R3OVy5LVD5Xrx+h/E+Cs2cDHReAqrQUOGAOIqd/9Tn5cXd7/wb27we6L0qZD+xIeFZmp37Fw9ZAnzXvaH1yIX8jIF3FV583PbNmScEdpu868AgfcgqPuC7wtxHavTs65w3l9wA7eePlA+8jIM33/B+XgWn2w42IuNjNh51FknGP9xGwaWP0zhsGByXhDe8BqF0jCY+Yjh89AjQ28ra1beyjLDc0HpKER8wt4EktP+mzczH67luiysqx7VUvJPrqS6KRG3odTd1dvrfV3gOw7kmi69f0jjmp4QOiVEpv0+jxx4h6/tTrFuqZp/U2XMjfMjhnDrBiBW+GilwJRrJAU5P10zZVvJS+8jJw6hTQ0gLcGAGWPmQ9UXKiuZlPfU9Jxgd2JCJRaSnR6V9uX9E+HlHfHCLalRl7pQs1PES0qEZv06WiDcBzz+oOTqaPPtTb86BwngkWS12dJFxw9Sqw613J+Ke4ACxZAiyYL5kAqbhXEi7IZID+fsn4Z/JJ0Gx2fubJafFiYN9e3vt3WuWjsm7fGkgOa7h5DWbW+JMn+BT3lxQK9fXAJx9LpgjOngWW86Trdc+gYd8LE+r5zfp96FYD/USb+Z7Pb9ssh5s2EjX9SPTvsF7PVm7EWiLz6wcg5wDMmEF0+ZLeIa96/z1r9i/8rYoKou2vEWXZUa1e49fj6wQg5wC8/ZbeGb9qbyN6YSvRgvlEM2cSzS0jquWzffNx/fvX/iFKp/U++tTEc0BlBdDVBZSVSUFImNfe5v1hKiUFCvWvAp9+LplgmXgVMC8VwnbeYCZZJ+fNgemzLyQTPPoIWPgA0N4OlJRIQUSYU+JqPnUGuOwVoo+APXuid/4EL5treaMUovOG8SPg/vuAAwedh2VYmH9k+P0ScPgwH5qOW9NUyPg7Df4PiPYsMAVIAiA2tiQBEBtbkgCIjS1JAMTGliQAYmNLEgCxMQX4DxvJZiayMybCAAAAAElFTkSuQmCC'

#draw the main viewer
root = Tk()
favicon = PhotoImage(data=encoded_string)
root.iconphoto(True, favicon) #sets the favicon for root and all toplevel()
root.title('Power Tools Test Manager')
running = True

#procedure to be taken when attempting to exit the program, which will prompt a save
def exitProgram():
    global running
    response = messagebox.askyesnocancel("Power Tools Test Manager", "Save before closing Test Manager?", parent=root.focus_get())
    if not response is None:
        if response:
            saveSession()
        running = False

root.protocol('WM_DELETE_WINDOW', exitProgram) #Override close button with exitProgram

#keep track of if the software is locked, if it is locked by password, and the password itself
locked = 0
passLocked = 0
password = ""

#class Theme, which holds values for the colors and styles that the program should use for all widgets.  Default values approximate Tkinter defaults.
class Theme:
    def __init__(self, colorsTitle="Default Gray", fontSizeTitle="Medium", fontTitle="Sans-Serif", bg="gray95", fg="black", contrastbg="white", contrastfg="black", selectbg="#00a2ed", selectfg="white", contrastselectbg="#00a2ed", contrastselectfg="white", fontSize=9, font="Helvetica"):
        #inititalize theme identifiers
        self.colorsTitle = colorsTitle
        self.fontSizeTitle = fontSizeTitle
        self.fontTitle = fontTitle

        #inititalize values
        self.bg = bg #colors to be used for most elements
        self.fg = fg
        self.contrastbg = contrastbg #colors to be used for elements that need to stand out from the background
        self.contrastfg = contrastfg
        self.selectbg = selectbg #colors used when highlighting text
        self.selectfg = selectfg
        self.contrastselectbg = contrastselectbg #colors used when highlighting text on contrast element
        self.contrastselectfg = contrastselectfg
        self.fontSize = fontSize
        self.font = font

    #Theme.apply, passing this method a common widget will automatically reconfigure its color and font to fit the theme
    def apply(self, widget):
        if isinstance(widget, list):  #if passed a list of widgets, recursively handle all widgets
            for oo in widget:
                self.apply(oo)
        if isinstance(widget, Tk) or isinstance(widget, Toplevel):
            widget.config(bg=self.bg)
        elif isinstance(widget, Frame):
            widget.config(bg=self.bg)
        elif isinstance(widget, LabelFrame):
            widget.config(bg=self.bg, fg=self.fg, font=(self.font, self.fontSize+2))
        elif isinstance(widget, Label):
            widget.config(bg=self.bg, fg=self.fg, font=(self.font, self.fontSize))
        elif isinstance(widget, Button) or isinstance(widget, Menubutton):
            widget.config(bg=self.bg, fg=self.fg, activebackground=self.bg, activeforeground=self.fg, font=(self.font, self.fontSize))
        elif isinstance(widget, Entry):
            widget.config(bg=self.contrastbg, fg=self.contrastfg, selectbackground=self.contrastselectbg, selectforeground=self.contrastselectfg, font=(self.font, self.fontSize))
        elif isinstance(widget, SelectLabel): #This conditional must come before Text, because SelectLabel extends Text
            widget.config(bg=self.bg, fg=self.fg, selectbackground=self.selectbg, selectforeground=self.selectfg, font=(self.font, self.fontSize))
        elif isinstance(widget, Text):
            widget.config(bg=self.contrastbg, fg=self.contrastfg, selectbackground=self.contrastselectbg, selectforeground=self.contrastselectfg, font=(self.font, self.fontSize))
        elif isinstance(widget, Checkbutton) or isinstance(widget, Radiobutton):
            widget.config(bg=self.bg, fg='black', activebackground=self.bg, activeforeground=self.bg, font=(self.font, self.fontSize))
        elif isinstance (widget, Menu):
            widget.config(bg=self.contrastbg, fg=self.contrastfg, activebackground=self.contrastselectbg, activeforeground=self.contrastselectfg, disabledforeground=None, font=(self.font, self.fontSize))
        return widget

#create a Theme object
T = Theme()

#class Test, holds all information about one test
class Test:
    #a separate tuple array to keep track of all comments in chronological order
    allComments = []

    #station status constants
    NORMAL = "In Progress"
    IN_PROGRESS = NORMAL
    PAUSED = "Paused"
    STOPPED = "Stopped"
    OFFLINE = "Offline"

    #Constructor which creates a test with expandable data
    def __init__(self, url, testNum, title="[title]", subtitle="[subtitle]"):
        global dataFrame

        self.id = url #unique identifying string used as a url 

        self.name = title #title of the station, should include name of unit and test type, should be identifiably unique
        self.serial = subtitle #subtitle for the station
        self.status = Test.OFFLINE
        self.data = [] #data variables, a len 32 list of 4-lists, including a string defining the datum, a string defining the units, the number datum, and a boolean which determines if the datum is used
       
        self.controls = [] #controls, a len 32 list of 2-lists, including a string name which communicates what each control does, and a boolean value

        self.comments = [] #tuple list of additional notes, including error modes and manual measurements
        #contains a string representing time of report, and a string phrase description
        self.r = None #row that the test is drawn to in the main viewer
        self.c = None #column that the test is drawn to in the main viewer
        #boolean which allows the test to be hidden
        self.showTest = True
        
        #initialize labelWidgetFrame and its children.  This widget will show the title of the station and a small edit button
        self.labelWidgetFrame = Frame()
        self.stationNumLabel = Label(self.labelWidgetFrame)
        self.stationNumLabel.grid(row=0, column=0)

        #initialize frame, which will be used to store the widgets
        self.frame = LabelFrame(dataFrame, labelwidget=self.labelWidgetFrame, padx=5, pady=5, relief=RIDGE)

        #initialize dataLabel, which will be used to display info
        self.dataLabel = SelectLabel(self.frame)
        #initialize statusIndicator, which will be used to visually represent the status of the test
        self.statusIndicator = Label(self.frame)

        #initialize two buttons, which will be used for test control
        self.button2 = Button(self.frame, width=14)

        #plot each widget into the frame
        self.dataLabel.grid(row=1)
        self.statusIndicator.grid(row=2, pady=2)
        #draw control button
        self.button2.grid(row=5)
    
       
    #Test.draw, draws the information to the screen based on internal info
    #parameters are positional info which will determine where it is drawn
    def draw(self, r, c):
        global locked
        global dataFrame
        self.r = r
        self.c = c

        #apply theme to all widgets
        T.apply([self.labelWidgetFrame, self.stationNumLabel, self.frame, self.dataLabel, self.statusIndicator, self.button2])

        self.stationNumLabel.config(text="Station " + str(self.testNum), font=(T.font, T.fontSize+2))
        self.frame.grid(row=r, column=c, pady=3, padx=3) #regrid the frame

        #add correct information to widgets
        self.updateLabel()
        

    def redraw(self):
        self.draw(self.r, self.c)
        
    #updateLabel, reconfigures the widgets within the gui frame to accurately represent and control the incoming data
    def updateLabel(self):
        global root
        self.dataLabel.config(text=self.toString())
        if self.status == Test.NORMAL:
            self.statusIndicator.config(text="\U00002B24   In Progress", fg="green")
            self.button2.config(text="Show Controls", command=lambda: openControls(self.testNum), state=NORMAL)
        elif self.status == Test.PAUSED:
            self.statusIndicator.config(text="\U00002B24   Paused", fg=T.fg)
            self.button2.config(text="Show Controls", command=lambda: openControls(self.testNum), state=NORMAL)
        elif self.status == Test.STOPPED:
            self.statusIndicator.config(text="\U00002B24   Stopped", fg="orange")
            self.button2.config(text="Show Controls", command=lambda: openControls(self.testNum), state=NORMAL)
        elif self.status == Test.OFFLINE:
            self.statusIndicator.config(text="\U00002B24   Offline", fg="red")
            self.button2.config(text="Show Controls", state=DISABLED)
        else: #in default state:
            self.statusIndicator.config(text=None)
            self.button2.config(text="Show Controls", state=DISABLED)

        #reconfigure the minimum size of the main window
        root.update_idletasks()
        root.minsize(width=max(root.winfo_reqwidth(),400), height=max(root.winfo_reqheight(),300))

    def setData(self, newData):
        #handle given data, making sure that each entry is a proper 4-list  
        self.data = [] 
        for oo in newData:
            self.data.append(["", "", 0, False])
            if ii < len(oo):
                if isinstance(oo, list):
                    if len(oo) > 0:
                        if isinstance(oo[0], str):
                            self.data[-1][0] = oo[0] #set datum name, string
                            self.data[-1][3] = True #assume the data is used if it has a name
                            
                    if len(oo) > 1:
                        if isinstance(oo[1], str):
                            self.data[-1][1] = oo[1] #set datum unit, string
                           
                    if len(oo) > 2:
                        self.data[ii][2] = oo[2] #set datum value, currently accepts any value type
                           
                    if len(oo) > 3:
                        if isinstance(oo[3], bool):
                            self.data[-1][3] = oo[3] #set show datum, boolean
                           
                elif isinstance(oo, str):
                    self.data[ii][0] = oo #set datum name if only a string name is given
                    self.data[ii][3] = True #assume the data is used if it has a name
        self.updateLabel()

    def setControls(self, newControls):
        self.controls = []
        for oo in newControls:
            self.controls.append(["", False])
            if ii < len(oo):
                if isinstance(oo, list):
                    if len(oo) > 0:
                        if isinstance(oo[0], str):
                            self.controls[-1][0] = oo[0] #set control label, string
                    if len(oo) > 1:
                        if isinstance(oo[1], bool):
                            self.controls[-1][1] = oo[1] #set control status, string
                elif isinstance(controls[-1], str):
                    self.controls[-1][0] = oo #set control label if only a string name is given
        self.updateLabel()     

    #Test.toString, will return a text representation of the data in the Test object
    def toString(self):
        string = self.name+"\n"+self.serial+"\n"
        for ii in range(numberOfData):
            if self.data[ii][3]:
                string += str(self.data[ii][0])+": "+f'{self.data[ii][2]:.2f}'+" "+str(self.data[ii][1])+"\n"
        return string.rstrip()
            
#list which holds the array of tests, currently begins empty
tests = []
#Dictionary which will be used to link address to index in tests[]
testIndexDict = {}

                                  
def saveSession():
    try:
        #open *.JSON file using system dialog
        file = filedialog.asksaveasfile(parent=root, initialdir = "/", title = "Save As", filetypes = (("JSON Files","*.json"),), defaultextension="*.*")
    except OSError as e: #catch errors relating to opening the file
        messagebox.showerror("Power Tools Test Manager", "Could not save file", parent=root.focus_get())
    else:
        if not file is None:
            testList = []
            for oo in tests:
                testList.append({
                    "number":oo.testNum, 
                    "title":oo.name, 
                    "subtitle":oo.serial, 
                    "data":[{
                        "name":oo.data[ii][0],
                        "units":oo.data[ii][1],
                        "show":oo.data[ii][3]
                        } for ii in range(numberOfData)],

                    "controls":[{"name":oo.controls[ii][0]} for ii in range(numberOfControls)]
                    })
            json.dump(testList, file)
    finally:
        if not file is None:
            file.close()
        
def openSession():
    try:
        #open *.JSON file using system dialog
        file = filedialog.askopenfile(parent=root, initialdir = "/", title = "Open", filetypes = (("JSON Files","*.json"),))
    except OSError as e: #catch errors relating to opening the file
        messagebox.showerror("Power Tools Test Manager", "Could not open file", parent=root.focus_get())
    else:
        if not file is None:
            testList = json.load(file)
            try:
                for oo in testList:
                    tests.append(Test(
                        oo["number"], 
                        oo["title"], 
                        oo["subtitle"], 
                        [[
                            oo["data"][ii]["name"], 
                            oo["data"][ii]["units"], 
                            0, 
                            oo["data"][ii]["show"] 
                            ]for ii in range(numberOfData)], 
                        [oo["controls"][ii]["name"] for ii in range(numberOfControls)]
                        ))
            except TypeError as e: #old version file support
                for oo in testList:
                    if len(oo) >= 5: #prevent oob errors
                        tests.append(Test(oo[0], oo[1], oo[2], oo[3], oo[4]))
                    elif len(oo) >= 4: #0.5 version file support
                        tests.append(Test(oo[0], oo[1], oo[2], oo[3]))
                    else:
                        messagebox.showerror("Power Tools Test Manager", "Incompatible File", parent=root.focus_get())
    finally:
        if not file is None:
            file.close()
        update()
        
def connect():
    global main_url
    #setup the new menu
    connector = T.apply(Toplevel())
    connector.title('Enter URL')
    connector.grab_set() #make window modal
    connector.focus_set()

    

    #connects the program to the chosen COM port
    def connect():
        main_url = urlEntry.get()
        #TODO: test communication before letting the program connect
        connector.destroy()

    #draw url entry
    urlEntry = T.apply(Entry(connector, width=17))
    urlEntry.insert(0, main_url)
    urlEntry.grid(row=0, column=0, padx=5, pady=5)

    #connect Button
    connectButton = T.apply(Button(connector, text='Save', command=connect))
    connectButton.grid(row=0, column=2, padx=5, pady=5)

    #close button
    T.apply(Button(connector, text='Cancel', command=connector.destroy)).grid(row=0, column=3, padx=5, pady=5)

    #set min window size
    connector.update_idletasks()
    connector.minsize(width=max(connector.winfo_reqwidth(),0), height=max(connector.winfo_reqheight(),0))

#changeView, opens a dialog which allows the user to choose which tests are drawn on the screen    
def changeView():
    global tests
    
    #setup the new menu
    view = T.apply(Toplevel())
    view.title("Select Stations")
    view.grab_set() #make window modal
    view.focus_set()

    T.apply(Label(view, text="Select stations")).pack(side=TOP)

    topFrame = T.apply(LabelFrame(view, bd=0))
    topFrame.pack(side=TOP)

    botFrame = T.apply(LabelFrame(view, bd=0))
    botFrame.pack(side=BOTTOM)

    get = []

    #list of all labels
    l = []
    #response list of IntVar()
    r = []
    #list of all checkbuttons
    c = []

    def refresh():
        nonlocal get
        nonlocal l, r, c
        #get = requests.get(main_url + 'index')
        get = [{ #temp data
            'url':'hjfsdfsad',
            'number':1,
            'title':"Demo Test 1",
            'subtitle':''
        }]
        #list of all labels
        l = []
        #response list of IntVar()
        r = []
        #list of all checkbuttons
        c = []
        #draw the set of checkboxes to the screen
        for oo in get:
            l.append(T.apply(SelectLabel(topFrame, text='Station '+oo['number']+'\n'+oo['title']+'\n'+oo['subtitle'])))
            r.append(IntVar())
            if oo['url'] in [o1.id for o1 in tests]:
                r[-1].set(1)
            c.append(T.apply(Checkbutton(topFrame, text=None, variable=r[-1], onvalue=1, offvalue=0, padx=10)))

            l[-1].grid(row=i%10, column=(i//10)*2)
            c[-1].grid(row=i%10, column=(i//10)*2+1)
            
            if r[i].get() == 1:
                c[i].select()
        
    #save changes made during the dialog
    def save():
        tests = []
        for ii in range(len(get)):
            if r[ii]:
                tests.append(Test(get[ii]['url'], get[ii]['number'], get[ii]['title'], get[ii]['subtitle']))
        update()
        view.destroy()
        
    #quickly selects all tests
    def selectAll():
        nonlocal c
        for oo in c:
            oo.select()
    #quickly deselects all tests   
    def deselectAll():
        nonlocal c
        for oo in c:
            oo.deselect()
            
    #cancel button
    T.apply(Button(botFrame, text="Cancel", command=view.destroy).grid(row=0, column=3, padx=5, pady=5))
    #save button
    T.apply(Button(botFrame, text="Save", command=save).grid(row=0, column=2, padx=5, pady=5))
    #Select All button
    T.apply(Button(botFrame, text="Select All", command=selectAll).grid(row=0, column=0, padx=5, pady=5))
    #Deselect All button
    T.apply(Button(botFrame, text="Deselect All", command=deselectAll).grid(row=0, column=1, padx=5, pady=5))
    #Refresh Button
    T.apply(Button(botFrame, text="Refresh", command=refresh).grid(row=1, column=1, padx=5, pady=5))

    view.update_idletasks()
    view.minsize(width=max(view.winfo_reqwidth(),300), height=max(view.winfo_reqheight(),200))

#writeToFile, allows the user to store current test information in a .txt file of their choice
def writeToFile():
    global tests
    #setup the new menu
    writer = T.apply(Toplevel())
    writer.title("Write To File")
    writer.grab_set() #make window modal
    writer.focus_set()

    T.apply(Label(writer, text="Selected stations will appear on the file")).pack(side=TOP)

    topFrame = T.apply(LabelFrame(writer, bd=0))
    topFrame.pack(side=TOP)

    botFrame = T.apply(LabelFrame(writer, bd=0))
    botFrame.pack(side=BOTTOM)
    
    #dictionary linking option name to internal index
    l = []
    #response list of IntVar()
    r = []
    #list of all checkbuttons
    c = []
    #draw the set of checkboxes to the screen
    for i in range(len(tests)):
        option = "Station "+str(tests[i].testNum)+": "+tests[i].name
        l.append(T.apply(SelectLabel(topFrame, text=option)))
        r.append(IntVar())
        r[i].set(tests[i].showTest)
        c.append(T.apply(Checkbutton(topFrame, text=None, variable=r[i], onvalue=1, offvalue=0, padx=10)))

        l[-1].grid(row=i%10, column=(i//10)*2)
        c[-1].grid(row=i%10, column=(i//10)*2+1)
        
        if r[i].get() == 1:
            c[i].select()

    ctVar = BooleanVar()
    commentToggle = T.apply(Checkbutton(writer, text = "Include Comments?", variable = ctVar, onvalue=1, offvalue=0, padx=0))
    commentToggle.pack(side=BOTTOM)
    commentToggle.select()
        
    #writes specified info to file
    def save():
        try:
            #open *.txt file using system dialog
            file = filedialog.asksaveasfile(parent=writer, initialdir = "/", title = "Save As", filetypes = (("Text Files","*.txt"),), defaultextension="*.*")
        except OSError as e: #catch errors relating to opening the file
            messagebox.showerror("Power Tools Test Manager", "Could not open file", parent=root.focus_get())
        else:
            if not file is None:
                file.write("Snap-On Test Manager, Version "+version+"\n")
                file.write(datetime.now().strftime("Data Captured on %m/%d/%Y at %H:%M:%S"))
                for i in range(len(r)):
                    if r[i].get() == 1:
                        if ctVar.get():
                            file.write("\n\nStation "+str(tests[i].testNum)+": "+str(tests[i].toStringPlusComments()))
                        else:
                            file.write("\n\nStation "+str(tests[i].testNum)+": "+str(tests[i].toString()))
                writer.destroy()
        finally:
            if not file is None:
                file.close()
        
    #quickly selects all tests
    def selectAll():
        nonlocal c
        for i in range(len(c)):
            c[i].select()
            
    #quickly deselects all tests   
    def deselectAll():
        nonlocal c
        for i in range(len(c)):
            c[i].deselect()
            
    #cancel button
    T.apply(Button(botFrame, text="Cancel", command=writer.destroy)).grid(row=2, column=3, padx=5, pady=5)
    #save button
    T.apply(Button(botFrame, text="Save As", command=save)).grid(row=2, column=2, padx=5, pady=5)
    #Select All button
    T.apply(Button(botFrame, text="Select All", command=selectAll)).grid(row=2, column=0, padx=5, pady=5)
    #Deselect All button
    T.apply(Button(botFrame, text="Deselect All", command=deselectAll)).grid(row=2, column=1, padx=5, pady=5)

    #set window minimum size
    writer.update_idletasks()
    writer.minsize(width=max(writer.winfo_reqwidth(),300), height=max(writer.winfo_reqheight(),200))


   
#openControls(): This function opens a new child window which will allow the user to see the status of the selected station's
#control coils
#if given a valid TestNum from an existing station, the window will start with that station selected
def openControls(InitialTestNum=0):
    global tests
    global testIndexDict
    if len(tests) == 0:
        messagebox.showerror("Power Tools Test Manager", "There are no stations added", parent=root.focus_get())
        return
    #setup the new menu
    tl = T.apply(Toplevel())
    tl.title("Label Controls")
    tl.grab_set() #make window modal
    tl.focus_set()

    topFrame = T.apply(Frame(tl, bd=0))
    topFrame.pack(side=TOP)

    midFrame = T.apply(Frame(tl, bd=0))
    midFrame.pack(side=TOP)

    botFrame = T.apply(Frame(tl, bd=0))
    botFrame.pack(side=BOTTOM)

    if InitialTestNum in testIndexDict:
        currentTestIndex=testIndexDict[InitialTestNum]
    else:
        currentTestIndex=-1

    #Building an array of the interactable objects
    numLabel = []
    controlButtons = []
    controlNameLabels = []
    for ii in range(numberOfControls):
        numLabel.append(T.apply(Label(midFrame, text=str(ii+1))))
        controlButtons.append(T.apply(Button(midFrame, width=8)))
        controlNameLabels.append(Label(midFrame, width=10, bg=T.contrastbg, fg=T.contrastfg, font=(T.font, T.fontSize), justify=LEFT))

        numLabel[ii].grid(row=(ii%16+3), column=(int(ii/16)*4))
        controlButtons[ii].grid(row=(ii%16+3), column=(int(ii/16)*4+1))
        controlNameLabels[ii].grid(row=(ii%16+3), column=(int(ii/16)*4+2), padx=5)

    
    def sendCommand(controlIndex, value):
        control(tests[currentTestIndex].testNum, controlIndex, value)
        update(currentTestIndex)


    dropdown = T.apply(Menubutton(topFrame, text="[default]", relief=RAISED))

    #update() is called whenever a new selection is made on the dropdown menu.  It reconfigures the window to reflect what was chosen.
    #if update() is passed an invalid index, then it will show a default selection
    def update(testIndex):
        nonlocal currentTestIndex
        currentTestIndex=testIndex
        if (currentTestIndex>=0): 
            dropdown.config(text=("Station "+str(tests[testIndex].testNum)+": "+tests[testIndex].name+" \U000025BC"))

            retryCount = 0
            done = False
            while not done:  #If the data retrieval is unsuccessful, Try three times before showing that the PLC is offline
                retSuccess, newControlStatus = retrieveControlStatus(tests[currentTestIndex].testNum)
                if retSuccess:  #The data retrieval has been successful.  Exit the loop and populate controls with current data
                    done = True
                    tests[currentTestIndex].setControlStatus(newControlStatus)
                    for ii in range(numberOfControls):
                        if newControlStatus[ii]:         
                            controlButtons[ii].config(text="ON", fg="green", state=NORMAL, command=lambda x=ii: sendCommand(x+1, 0))
                        else:
                            controlButtons[ii].config(text="OFF", fg=T.fg, state=NORMAL, command=lambda x=ii: sendCommand(x+1, 1))
                else:
                    retryCount += 1 #try again

                if retryCount >= 3:  #The data retrieval has been unsuccessful three times.  Exit the loop and show controls offline
                    done = True
                    tests[currentTestIndex].setOffline()
                    for ii in range(numberOfControls):
                        controlButtons[ii].config(text="OFFLINE", fg=T.fg, state=DISABLED, command=None)

            for ii in range(numberOfControls):
                controlNameLabels[ii].config(text=tests[currentTestIndex].controls[ii][0])
                if tests[currentTestIndex].status == Test.OFFLINE:
                    controlButtons[ii].config(text="OFFLINE", fg=T.fg, state=DISABLED, command=None)
                else:
                    if tests[currentTestIndex].controls[ii][1]:
                        controlButtons[ii].config(text="ON", fg="green", state=NORMAL, command=lambda x=ii: sendCommand(x+1, 0))
                    else:
                        controlButtons[ii].config(text="OFF", fg=T.fg, state=NORMAL, command=lambda x=ii: sendCommand(x+1, 1))                
                        
        else:
            dropdown.config(text=("Choose a station to control \U000025BC"))
            for ii in range(numberOfControls):
                controlNameLabels[ii].config(text="")
                controlButtons[ii].config(text="", state=DISABLED)

    #close the current window and open the control label editor for the selected test
    def openControlEditor():
        tl.destroy()
        if currentTestIndex>=0:
            editControls(tests[currentTestIndex].testNum)
        else:
            editControls()
        
    #create and assign a menu to the dropdown menubutton.  This menu will allow the user to select which station they want to control.
    dropdown.menu = T.apply(Menu(dropdown, tearoff=0))
    dropdown["menu"] = dropdown.menu
    for ii in range(len(tests)):
        dropdown.menu.add_command(label=("Station "+str(tests[ii].testNum)+": "+tests[ii].name), command=lambda x=ii: update(x))
    dropdown.grid()

    update(currentTestIndex) #populate the screen for the first time

    T.apply(Button(botFrame, text="Edit Labels", command=openControlEditor)).grid(row=0, column=0, padx=5, pady=5)

    #refresh button
    T.apply(Button(botFrame, text="Refresh", command=lambda: update(currentTestIndex))).grid(row=0, column=1, padx=5, pady=5)

    #cancel button
    T.apply(Button(botFrame, text="Close", command=tl.destroy)).grid(row=0, column=3, padx=5, pady=5)
    
    #set min window size
    tl.update_idletasks()
    tl.minsize(width=max(tl.winfo_reqwidth(),300), height=max(tl.winfo_reqheight(),200))



#theme():  This function opens a window that will allow the user to select which colors, font, and text size the program uses
#As new selections are made, this window will be updated to give the user a preview of the theme they have selected
def theme():
    global T
    #initialize a new Theme() object based on the current global Theme
    newTheme=copy.deepcopy(T)

    #setup the new menu
    tl = newTheme.apply(Toplevel())
    tl.title("Configure Appearance")
    tl.grab_set() #make window modal
    tl.focus_set()

    topFrame = newTheme.apply(Frame(tl, bd=0))
    topFrame.pack(side=TOP)

    midFrame = newTheme.apply(Frame(tl, bd=0))
    midFrame.pack(side=TOP)

    botFrame = newTheme.apply(Frame(tl, bd=0))
    botFrame.pack(side=BOTTOM)

    terse = newTheme.apply(SelectLabel(topFrame, text="Current Theme: "+newTheme.colorsTitle+", "+newTheme.fontSizeTitle+" "+newTheme.fontTitle))
    terse.pack()

    def refresh():
        newTheme.colorsTitle = colorsVar.get().strip()
        if newTheme.colorsTitle == "Default Gray":
            newTheme.bg="gray95"
            newTheme.fg="black"
            newTheme.contrastbg="white"
            newTheme.contrastfg="black"
            newTheme.selectbg="#00a2ed"
            newTheme.selectfg="white"
            newTheme.contrastselectbg=newTheme.selectbg
            newTheme.contrastselectfg=newTheme.selectfg
        elif newTheme.colorsTitle == "Monochrome":
            newTheme.bg="white"
            newTheme.fg="black"
            newTheme.contrastbg="gray90"
            newTheme.contrastfg="black"
            newTheme.selectbg="gray"
            newTheme.selectfg="black"
            newTheme.contrastselectbg=newTheme.selectbg
            newTheme.contrastselectfg=newTheme.selectfg
        elif newTheme.colorsTitle == "Mint":
            newTheme.bg="#dbeed7"
            newTheme.fg="#3f000f"
            newTheme.contrastbg="white"
            newTheme.contrastfg="#3f000f"
            newTheme.selectbg="#3f000f"
            newTheme.selectfg="white"
            newTheme.contrastselectbg=newTheme.selectbg
            newTheme.contrastselectfg=newTheme.selectfg
        elif newTheme.colorsTitle == "Night":
            newTheme.bg="#1d2951"
            newTheme.fg="white"
            newTheme.contrastbg="slategray"
            newTheme.contrastfg="white"
            newTheme.selectbg="white"
            newTheme.selectfg="slategray"
            newTheme.contrastselectbg=newTheme.selectbg
            newTheme.contrastselectfg=newTheme.selectfg
        elif newTheme.colorsTitle == "Two-Tone":
            newTheme.bg="black"
            newTheme.fg="white"
            newTheme.contrastbg="white"
            newTheme.contrastfg="black"
            newTheme.selectbg="white"
            newTheme.selectfg="black"
            newTheme.contrastselectbg="black"
            newTheme.contrastselectfg="white"

        newTheme.fontSizeTitle = fontSizeVar.get().strip()
        if newTheme.fontSizeTitle == "Small":
            newTheme.fontSize = 7
        elif newTheme.fontSizeTitle == "Medium":
            newTheme.fontSize = 9
        elif newTheme.fontSizeTitle == "Large":
            newTheme.fontSize = 11
        elif newTheme.fontSizeTitle == "Extra Large":
            newTheme.fontSize = 13

        newTheme.fontTitle = fontVar.get().strip()
        if newTheme.fontTitle == "Sans-Serif":
            newTheme.font = "Helvetica"
        elif newTheme.fontTitle == "Serif":
            newTheme.font = "Times"
        elif newTheme.fontTitle == "Monospaced":
            newTheme.font = "Courier"

        newTheme.apply(tl)
        newTheme.apply(topFrame)
        newTheme.apply(midFrame)
        newTheme.apply(botFrame)
        newTheme.apply(terse)
        terse.config(text="Current Theme: "+newTheme.colorsTitle+", "+newTheme.fontSizeTitle+" "+newTheme.fontTitle)
        newTheme.apply([colorsHeader, fontSizeHeader, fontHeader, saveButton, cancelButton])
        for oo in r:
            newTheme.apply(oo)
        for oo in l:
            newTheme.apply(oo)

    r = [] #list of all radiobuttons
    l = [] #list of all accompanying labels

    colorsVar = StringVar(value=newTheme.colorsTitle)
    colorsOptions = ["Default Gray", "Monochrome", "Mint", "Night", "Two-Tone"]
    colorsHeader = newTheme.apply(SelectLabel(midFrame, text="Color theme:"))
    colorsHeader.grid(row=0, column=1, columnspan=1)

    for ii in range(len(colorsOptions)):
        r.append(newTheme.apply(Radiobutton(midFrame, variable=colorsVar, value=colorsOptions[ii], command=refresh)))
        l.append(newTheme.apply(SelectLabel(midFrame, text=colorsOptions[ii])))

        r[-1].grid(row=ii+1, column=0)
        l[-1].grid(row=ii+1, column=1)

    fontSizeVar = StringVar(value=newTheme.fontSizeTitle)
    fontSizeOptions = ["Small", "Medium", "Large", "Extra Large"]
    fontSizeHeader = newTheme.apply(SelectLabel(midFrame, text="Text Size:"))
    fontSizeHeader.grid(row=0, column=3, columnspan=1)

    for ii in range(len(fontSizeOptions)):
        r.append(newTheme.apply(Radiobutton(midFrame, variable=fontSizeVar, value=fontSizeOptions[ii], command=refresh)))
        l.append(newTheme.apply(SelectLabel(midFrame, text=fontSizeOptions[ii])))

        r[-1].grid(row=ii+1, column=2)
        l[-1].grid(row=ii+1, column=3)

    fontVar = StringVar(value=newTheme.fontTitle)
    fontOptions = ["Sans-Serif", "Serif", "Monospaced"]
    fontHeader = newTheme.apply(SelectLabel(midFrame, text="Font Family:"))
    fontHeader.grid(row=len(fontSizeOptions)+1, column=3, columnspan=1)

    for ii in range(len(fontOptions)):
        r.append(newTheme.apply(Radiobutton(midFrame, variable=fontVar, value=fontOptions[ii], command=refresh)))
        l.append(newTheme.apply(SelectLabel(midFrame, text=fontOptions[ii])))

        r[-1].grid(row=ii+len(fontSizeOptions)+2, column=2)
        l[-1].grid(row=ii+len(fontSizeOptions)+2, column=3)


    def save():
        global T
        T = newTheme
        update()
        tl.destroy()

    #save button
    saveButton = Button(botFrame, text="Save", command=save)
    saveButton.grid(row=0, column=0, padx=5, pady=5)

    #cancel button
    cancelButton = Button(botFrame, text="Cancel", command=tl.destroy)
    cancelButton.grid(row=0, column=3, padx=5, pady=5)

    #set min window size
    tl.update_idletasks()
    tl.minsize(width=max(tl.winfo_reqwidth(),300), height=max(tl.winfo_reqheight(),200))

#declaring dataFrame, which will hold all test widgets
dataFrame = LabelFrame(root, bd=0)
dataFrame.pack(side=TOP)

#Version label in the far right, on a window-spanning relief bar
ver = Frame(root, bd=1, relief=SUNKEN)
verText = Label(ver, text="version " + version)
verText.pack(side=RIGHT)
ver.pack(side=BOTTOM, fill='x')


#build the windows-style menubar with multiple cascades #TODO: weird line?? Fonts not working???
menubar = Menu(root)

fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label="Save Session", command=saveSession)
fileMenu.add_command(label="Open Session", command=openSession)
fileMenu.add_command(label="Connect to Port", command=connect)
fileMenu.add_command(label="Write to File", command=writeToFile)
fileMenu.add_command(label="Exit", command=exitProgram)
menubar.add_cascade(label="File", menu=fileMenu)

viewMenu = Menu(menubar, tearoff=0)
viewMenu.add_command(label="Select Stations", command=changeView)
viewMenu.add_command(label="Theme", command=theme)
viewMenu.add_command(label="Show Controls", command=openControls)
menubar.add_cascade(label="View", menu=viewMenu)

root.config(menu=menubar)

#Draws the screen with the current parameters
def update():
    global root
    global dataFrame
    global testIndexDict
    #apply appearance theme to main window
    T.apply([root, dataFrame, ver])
    verText.config(bg=T.bg, fg=T.fg, font=(T.font, T.fontSize-2, "italic"))

    #forget all children in anticipation of reordering and redrawing them
    for child in dataFrame.winfo_children():
        child.grid_forget()
    placer = 0
    tests.sort(key=lambda x: x.testNum) #sort tests by test number/slave address
    testIndexDict = {} #reset dictonary
    for i in range(len(tests)):
        testIndexDict[tests[i].testNum] = i
        
        if tests[i].showTest:
            tests[i].draw(int(placer/10)+1, placer%10)
            placer += 1
        

    T.apply([fileMenu, viewMenu])

    root.update_idletasks()
    root.geometry(str(max(root.winfo_reqwidth(),400))+'x'+str(max(root.winfo_reqheight(),300)))
    root.minsize(width=max(root.winfo_reqwidth(),400), height=max(root.winfo_reqheight(),300))

           
#draw screen for the first time
update()

              
#main loop for recieving checking up and recieving from PLCs and continuing the GUI
#if the loop encounters an error while parsing three times in a row, it will mark the test as offline and proceed to poll the next test
while(running): #root.state() == 'normal'):
    
    root.update() #maintain root window
    
root.destroy()

#root.mainloop()
