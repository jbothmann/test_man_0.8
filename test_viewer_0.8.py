from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkSelectLabel import * #Local Import
from datetime import datetime
from time import sleep
import requests

import json
import copy
import os
import string
import random
import tkTheme #Local Import
import tkinter.font
import threading

version = "0.8"

pollPeriod = 0.01 #in seconds

pollTimeout = 0.01

main_url = ""

numberOfData = 32
numberOfControls = 32

#base64 encoded bytestring which contains the favicon
encoded_string = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASQSURBVHhe7ZpdbBRVFMf/K61AgFKxfegmoA9SC0E0JGCIBqg0giH6Ag+KL2BEjU3E+PEkbJAHNDHVaAL4EYUH06A+iAFMSSG8WROFAm2wHyDGpppAhLZJW+luOZ7LnAnb7el054tpnPml/5x77+69e8+ZO/djpikC+C++3CU2tiQBEBtbkgCIjS1JAMTGliQAYmNLEgCxsSUJgNjYcmdOg6WlwPp1wIYNQHU1h32afMA/ffOmpBmTtntDJp3XtdFRSTCm3P7M2MI2bG61l/e9N94EenqsvI00FZ7q1hJ1dhCN5qLV0SNq/8IdAS+9COzdx1c84jstmwWWLQMu/CYFtwmvZ2tWTw3nDQcPqM4bwhkBd/M939oK1NRIQYQMDAAPcj+uXJGCsYRzebZtmxrOGxoaJnTeEPwImDcP6OywbNT09loXYmhYCsYT/AjI7Jgazht2vOPovCHYEWDW+PPnrHXfiWPHLOVyUhAQ5eXAqlW851gPtJ0Hlj/K3k3inglAYPrhe30NzlfbOaLp0/X6QenhpUQrV+qfFSi4ADxRqzucr6FBq3Na/YgUTABKSohaz+hO5+v17Xr9CBVMALZu0R3OVy5LVD5Xrx+h/E+Cs2cDHReAqrQUOGAOIqd/9Tn5cXd7/wb27we6L0qZD+xIeFZmp37Fw9ZAnzXvaH1yIX8jIF3FV583PbNmScEdpu868AgfcgqPuC7wtxHavTs65w3l9wA7eePlA+8jIM33/B+XgWn2w42IuNjNh51FknGP9xGwaWP0zhsGByXhDe8BqF0jCY+Yjh89AjQ28ra1beyjLDc0HpKER8wt4EktP+mzczH67luiysqx7VUvJPrqS6KRG3odTd1dvrfV3gOw7kmi69f0jjmp4QOiVEpv0+jxx4h6/tTrFuqZp/U2XMjfMjhnDrBiBW+GilwJRrJAU5P10zZVvJS+8jJw6hTQ0gLcGAGWPmQ9UXKiuZlPfU9Jxgd2JCJRaSnR6V9uX9E+HlHfHCLalRl7pQs1PES0qEZv06WiDcBzz+oOTqaPPtTb86BwngkWS12dJFxw9Sqw613J+Ke4ACxZAiyYL5kAqbhXEi7IZID+fsn4Z/JJ0Gx2fubJafFiYN9e3vt3WuWjsm7fGkgOa7h5DWbW+JMn+BT3lxQK9fXAJx9LpgjOngWW86Trdc+gYd8LE+r5zfp96FYD/USb+Z7Pb9ssh5s2EjX9SPTvsF7PVm7EWiLz6wcg5wDMmEF0+ZLeIa96/z1r9i/8rYoKou2vEWXZUa1e49fj6wQg5wC8/ZbeGb9qbyN6YSvRgvlEM2cSzS0jquWzffNx/fvX/iFKp/U++tTEc0BlBdDVBZSVSUFImNfe5v1hKiUFCvWvAp9+LplgmXgVMC8VwnbeYCZZJ+fNgemzLyQTPPoIWPgA0N4OlJRIQUSYU+JqPnUGuOwVoo+APXuid/4EL5treaMUovOG8SPg/vuAAwedh2VYmH9k+P0ScPgwH5qOW9NUyPg7Df4PiPYsMAVIAiA2tiQBEBtbkgCIjS1JAMTGliQAYmNLEgCxMQX4DxvJZiayMybCAAAAAElFTkSuQmCC'

#draw the main viewer
root = Tk()
favicon = PhotoImage(data=encoded_string)
root.iconphoto(True, favicon) #sets the favicon for root and all toplevel()
root.title('Power Tools Test Viewer')

#procedure to be taken when attempting to exit the program, which will prompt a save
def exitProgram():
    global running
    response = messagebox.askyesno("Power Tools Test Viewer", "Exit Test Viewer?", parent=root.focus_get())
    if response:
        poll.stop()
        root.destroy()

root.protocol('WM_DELETE_WINDOW', exitProgram) #Override close button with exitProgram

#keep track of if the software is locked, if it is locked by password, and the password itself
locked = 0
passLocked = 0
password = ""

#create an empty list, to be filled with user-specified Theme objects from the themes.json config file.  Population occurs in startup configuration phase
themes = []
#create an empty list, to be filled with user-specified fonts from the fonts.json config file.  Population occurs in startup configuration phase
families = []
#create an empty list, to be filled with user-specified text sizes from the fonts.json config file.  Population occurs in startup configuration phase
sizes = []

#ThemeAndFont subclass that provides support for SelectLabels
class myThemeAndFont(tkTheme.ThemeAndFont):
    def apply(self, widget):
        if isinstance(widget, list):
            for oo in widget:
                self.apply(oo)
        elif isinstance(widget, SelectLabel):
            widget.config(bg=T.theme.bg, fg=T.theme.fg, selectbackground=T.theme.selectbg, selectforeground=T.theme.selectfg, font=(T.family, T.size))
        else:
            super().apply(widget)

        return widget

    __call__ = apply


#create a ThemeAndFont object, which we will use to paint our program #TODO: ThemeAndFont should be subclassed to override apply() to work with SelectLabels
T = myThemeAndFont()

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

        self.url = url #unique identifying string used as a url 

        self.testNum = testNum #slave id of the station
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

        self.online = True #boolean value that represents if the application has encountered any problems connecting to that url or not
        
        #initialize labelWidgetFrame and its children.  This widget will show the title of the station
        #connectionHint is a label that is normally empty, but will warn the user if the station becomes disconnected
        self.labelWidgetFrame = Frame()
        self.stationNumLabel = Label(self.labelWidgetFrame)
        self.stationNumLabel.grid(row=0, column=0)
        self.connectionHint = Label(self.labelWidgetFrame)
        self.connectionHint.grid(row=0, column=1)

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

        self.periodicCall() #Do first call and update to #TODO document
    
       
    #Test.draw, draws the information to the screen based on internal info
    #parameters are positional info which will determine where it is drawn
    def draw(self, r, c):
        global locked
        global dataFrame
        self.r = r
        self.c = c

        #apply theme to all widgets
        T.apply([self.labelWidgetFrame, self.stationNumLabel, self.connectionHint, self.frame, self.statusIndicator, self.button2])

        #apply non-contrast theme to SelectLabel() widget dataLabel
        self.dataLabel.config(bg=T.theme.bg, fg=T.theme.fg, selectbackground=T.theme.selectbg, selectforeground=T.theme.selectfg, font=(T.family, T.size))
        self.stationNumLabel.config(text="Station " + str(self.testNum), font=(T.family, T.size+2))
        self.connectionHint.config(fg = 'red')
        self.frame.grid(row=r, column=c, pady=3, padx=3) #regrid the frame

        #add correct information to widgets
        self.updateLabel()
        

    def redraw(self):
        self.draw(self.r, self.c)
        
    #updateLabel, reconfigures the widgets within the gui frame to accurately represent and control the incoming data
    def updateLabel(self):
        global root
        #Update data label to reflect current data
        self.dataLabel.config(text=self.toString())

        #Update status label to reflect current status, and update buttons to 
        if self.status == Test.NORMAL:
            self.statusIndicator.config(text="\U00002B24   In Progress", fg="green")
            self.button2.config(text="Show Controls", command=lambda: openControls(self.testNum), state=NORMAL)
        elif self.status == Test.PAUSED:
            self.statusIndicator.config(text="\U00002B24   Paused", fg=T.theme.fg)
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

        #update connectionHint to reflect connection status
        if self.online:
            self.connectionHint.config(text="")
        else:
            self.connectionHint.config(text="No Connection") #TODO: doesn't work

        #reconfigure the minimum size of the main window
        root.update_idletasks()
        root.minsize(width=max(root.winfo_reqwidth(),400), height=max(root.winfo_reqheight(),300))

    def periodicCall(self):
        if self.showTest == True:
            self.updateLabel()
        root.after(200, self.periodicCall) #schedule next call, in ms

    def setData(self, newData):
        #handle given data, making sure that each entry is a proper 4-list  
        self.data = [] 
        for oo in newData:
            self.data.append(["", "", 0, False])
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

            elif isinstance(oo, dict):
                if "name" in oo:
                    if isinstance(oo["name"], str):
                        self.data[-1][0] = oo["name"] #set datum name, string
                        self.data[-1][3] = True #assume the data is used if it has a name

                if "units" in oo:
                    if isinstance(oo["units"], str):
                        self.data[-1][1] = oo["units"] #set datum unit, string

                if "float" in oo:
                    if isinstance(oo["float"], float):
                        self.data[-1][2] = oo["float"] #set value, python float

                if "show" in oo:
                    if isinstance(oo["show"], bool):
                        self.data[-1][3] = oo["show"] #set show datum, boolean
                       
            elif isinstance(oo, str):
                self.data[ii][0] = oo #set datum name if only a string name is given
                self.data[ii][3] = True #assume the data is used if it has a name

    def setControls(self, newControls):
        self.controls = []
        for oo in newControls:
            self.controls.append(["", False])
            if isinstance(oo, list):
                if len(oo) > 0:
                    if isinstance(oo[0], str):
                        self.controls[-1][0] = oo[0] #set control label, string

                if len(oo) > 1:
                    if isinstance(oo[1], bool):
                        self.controls[-1][1] = oo[1] #set control status, boolean

            if isinstance(oo, dict):
                if "name" in oo:
                    if isinstance(oo["name"], str):
                        self.controls[-1][0] = oo["name"] #set control label, string

                if "bool" in oo:       
                    if isinstance(oo["bool"], bool):
                        self.controls[-1][1] = oo["bool"] #set control status, boolean

            elif isinstance(oo, str):
                self.controls[-1][0] = oo #set control label if only a string name is given 

    def setOnline(self):
        if not self.online:
            self.online = True

    def setOffline(self):
        if self.online:
            self.online = False


    #Test.toString, will return a text representation of the data in the Test object
    def toString(self):
        string = self.name+"\n"+self.serial+"\n"
        for ii in range(len(self.data)):
            if self.data[ii][3]:
                string += str(self.data[ii][0])+": "+f'{self.data[ii][2]:.2f}'+" "+str(self.data[ii][1])+"\n"
        return string.rstrip()
            
#list which holds the array of tests, currently begins empty
tests = []
#Dictionary which will be used to link address to index in tests[]
testIndexDict = {}

#connect(), opens a dialog which allows the user to enter the url that they want to connect to
def connect():
    global main_url
    #setup the new menu
    connector = T.apply(Toplevel())
    connector.title('Enter URL')
    connector.grab_set() #make window modal
    connector.focus_set()

    #connects the program to the chosen COM port
    def connect():
        global main_url
        global pollTimeout
        try:
            get = requests.get(urlEntry.get(), timeout = pollTimeout)
            get.raise_for_status()
            if not get.json()['app'] == "Power Tools Test Manager":
                raise Exception('wrong app')
            if not get.json()['version'] == version:
                raise Exception('wrong version')

        #TODO: allow url mutation after displaying error?
        except requests.exceptions.ConnectionError as e:
            messagebox.showerror("Power Tools Test Viewer", "That address could not be reached", parent=root.focus_get())
        except requests.exceptions.MissingSchema as e:
            messagebox.showerror("Power Tools Test Viewer", "The address supplied is not a valid url", parent=root.focus_get())
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Power Tools Test Viewer", "That address provided a bad response (Type H)", parent=root.focus_get())
        except requests.exceptions.Timeout as e:
            messagebox.showerror("Power Tools Test Viewer", "That address took too long to respond", parent=root.focus_get())
        except json.JSONDecodeError as e:
            messagebox.showerror("Power Tools Test Viewer", "That address provided a bad response (Type J)", parent=root.focus_get())
        except KeyError as e:
            messagebox.showerror("Power Tools Test Viewer", "That address provided a bad response (Type K)", parent=root.focus_get())
        except Exception as e:
            if 'wrong app' in e.args:
                messagebox.showerror("Power Tools Test Viewer", "That address is not serving a compatible application", parent=root.focus_get())
            elif 'wrong version' in e.args:
                messagebox.showerror("Power Tools Test Viewer", "That address is not serving a compatible version of Power Tools Test Manager", parent=root.focus_get())
            else:
                raise

        else:
            main_url = urlEntry.get()
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
    connector.minsize(width=max(connector.winfo_reqwidth(),225), height=max(connector.winfo_reqheight(),40))

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

        #forget all children in anticipation of reordering and redrawing them
        for child in topFrame.winfo_children():
            child.grid_forget()

        try:
            #make GET request to API server
            get = requests.get(main_url + 'index')
            #list of all labels
            l = []
            #response list of IntVar()
            r = []
            #list of all checkbuttons
            c = []
            #draw the set of checkboxes to the screen
            for oo in get.json():
                l.append(T.apply(SelectLabel(topFrame, text='Station '+str(oo['number'])+'\n'+str(oo['title'])+'\n'+str(oo['subtitle']), pady=5)))
                r.append(IntVar())
                if oo['url'] in [o1.url for o1 in tests]:
                    r[-1].set(1)
                c.append(T.apply(Checkbutton(topFrame, text=None, variable=r[-1], onvalue=1, offvalue=0, padx=5)))

                l[-1].grid(row=len(l)%5, column=(len(l)//5)*2)
                c[-1].grid(row=len(c)%5, column=(len(c)//5)*2+1)
                
                if r[-1].get() == 1:
                    c[-1].select()
        except Exception as e:
            messagebox.showerror("Power Tools Test Viewer", "An error occured while connecting to the index", parent=root.focus_get())

    refresh()
        
    #save changes made during the dialog
    def save():
        for ii in range(len(get.json())):
            if r[ii].get():
                tests.append(Test(get.json()[ii]['url'], get.json()[ii]['number'], get.json()[ii]['title'], get.json()[ii]['subtitle']))
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
    T.apply(Button(botFrame, text="Cancel", command=view.destroy)).grid(row=0, column=4, padx=5, pady=5)
    #save button
    T.apply(Button(botFrame, text="Save", command=save)).grid(row=0, column=3, padx=5, pady=5)
    #Select All button
    T.apply(Button(botFrame, text="Select All", command=selectAll)).grid(row=0, column=0, padx=5, pady=5)
    #Deselect All button
    T.apply(Button(botFrame, text="Deselect All", command=deselectAll)).grid(row=0, column=1, padx=5, pady=5)
    #Refresh Button
    T.apply(Button(botFrame, text="Refresh", command=refresh)).grid(row=0, column=2, padx=5, pady=5)

    view.update_idletasks()
    view.minsize(width=max(view.winfo_reqwidth(),300), height=max(view.winfo_reqheight(),200))

#removeAllStations, gives the user simple way to remove all stations from the screen, and also from polling
#calling this function will cease network activity until a new station is added
def removeAllStations():
    del tests[:]
    update()

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
    for ii in range(len(tests)):
        option = "Station "+str(tests[ii].testNum)+": "+tests[ii].name
        l.append(T.apply(SelectLabel(topFrame, text=option)))
        r.append(IntVar())
        r[ii].set(tests[ii].showTest)
        c.append(T.apply(Checkbutton(topFrame, text=None, variable=r[ii], onvalue=1, offvalue=0, padx=10)))

        l[-1].grid(row=ii%10, column=(ii//10)*2)
        c[-1].grid(row=ii%10, column=(ii//10)*2+1)
        
        if r[ii].get() == 1:
            c[ii].select()

    
        
    #writes specified info to file
    def save():
        try:
            #open *.txt file using system dialog
            file = filedialog.asksaveasfile(parent=writer, initialdir = "/", title = "Save As", filetypes = (("Text Files","*.txt"),), defaultextension="*.*")
        except OSError as e: #catch errors relating to opening the file
            messagebox.showerror("Power Tools Test Viewer", "Could not open file", parent=root.focus_get())
        else:
            if not file is None:
                file.write("Snap-On Test Viewer, Version "+version+"\n")
                file.write(datetime.now().strftime("Data Captured on %m/%d/%Y at %H:%M:%S"))
                for ii in range(len(r)):
                    if r[ii].get() == 1:
                        file.write("\n\nStation "+str(tests[ii].testNum)+": "+str(tests[ii].toString()))
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
    tl.title("Station Controls")
    tl.grab_set() #make window modal
    tl.focus_set()

    topFrame = T.apply(Frame(tl, bd=0))
    topFrame.pack(side=TOP)

    midFrame = T.apply(Frame(tl, bd=0))
    midFrame.pack(side=TOP)

    botFrame = T.apply(Frame(tl, bd=0))
    botFrame.pack(side=BOTTOM)

    #Set the test index from the dictionary using the InitialTestNum specified
    if InitialTestNum in testIndexDict:
        currentTestIndex=testIndexDict[InitialTestNum]
    else:
        currentTestIndex=-1

    #Building an array of display objects
    numLabel = []
    controlStatusLabels = []
    controlNameLabels = []
    for ii in range(numberOfControls):
        numLabel.append(T.apply(Label(midFrame, text=str(ii+1))))
        controlStatusLabels.append(T.apply(Label(midFrame, width=8)))
        controlNameLabels.append(SelectLabel(midFrame, width=14, height=1, bg=T.theme.contrast_bg, fg=T.theme.contrast_fg, font=(T.family, T.size), justify=LEFT, shrink=False))

        numLabel[ii].grid(row=(ii%16+3), column=(int(ii/16)*4))
        controlStatusLabels[ii].grid(row=(ii%16+3), column=(int(ii/16)*4+2))
        controlNameLabels[ii].grid(row=(ii%16+3), column=(int(ii/16)*4+1), padx=5)


    #refresh() is called whenever a new selection is made on the dropdown menu.  It reconfigures the window to reflect what was chosen.
    #if refresh() is passed an invalid index, then it will show a default selection
    def refresh(testIndex):
        nonlocal currentTestIndex
        
        currentTestIndex=testIndex
        if (currentTestIndex>=0): 
            dropdown.config(text=("Station "+str(tests[testIndex].testNum)+": "+tests[testIndex].name+" \U000025BC"))

            for ii in range(numberOfControls):
                if ii < len(tests[currentTestIndex].controls):
                    controlNameLabels[ii].config(text=tests[currentTestIndex].controls[ii][0])
                    if tests[currentTestIndex].status == Test.OFFLINE:
                        controlStatusLabels[ii].config(text="OFFLINE", fg="red")
                    else:
                        if tests[currentTestIndex].controls[ii][1]:
                            controlStatusLabels[ii].config(text="ON", fg="green")
                        else:
                            controlStatusLabels[ii].config(text="OFF", fg=T.theme.fg)
                else:
                    controlNameLabels[ii].config(text=" ")
                    controlStatusLabels[ii].config(text=" ")        
                        
        else:
            dropdown.config(text=("Select a Station \U000025BC"))
            for ii in range(numberOfControls):
                controlNameLabels[ii].config(text=" ")
                controlStatusLabels[ii].config(text=" ")

        
    #create and assign a menu to the dropdown menubutton.  This menu will allow the user to select which station they want to control.
    dropdown = T.apply(Menubutton(topFrame, text="[default]", relief=RAISED))
    dropdown.menu = T.apply(Menu(dropdown, tearoff=0))
    dropdown["menu"] = dropdown.menu
    for ii in range(len(tests)):
        dropdown.menu.add_command(label=("Station "+str(tests[ii].testNum)+": "+tests[ii].name), command=lambda x=ii: refresh(x))
    dropdown.grid()

    refresh(currentTestIndex) #populate the screen for the first time

    #refresh button
    T.apply(Button(botFrame, text="Refresh", command=lambda: refresh(currentTestIndex))).grid(row=0, column=1, padx=5, pady=5)

    #cancel button
    T.apply(Button(botFrame, text="Close", command=tl.destroy)).grid(row=0, column=3, padx=5, pady=5)
    
    #set min window size
    tl.update_idletasks()
    tl.minsize(width=max(tl.winfo_reqwidth(),300), height=max(tl.winfo_reqheight(),200))

#theme():  This function opens a window that will allow the user to select which colors, font, and text size the program uses
#As new selections are made, this window will be updated to give the user a preview of the theme they have selected
def theme():
    global T
    #initialize a new ThemeAndFont() object based on the current global Theme
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

    terse = newTheme.apply(SelectLabel(topFrame, text="Current Theme: %s, %i %s" % (newTheme.theme.title, newTheme.size, newTheme.family)))
    terse.pack()

    def refresh():
        newTheme.set(theme=next((oo for oo in themes if oo.title == colorsVar.get()), tkTheme.Theme()), family=fontVar.get(), size=fontSizeVar.get())

        newTheme.apply(tl)
        newTheme.apply(topFrame)
        newTheme.apply(midFrame)
        newTheme.apply(botFrame)
        newTheme.apply(terse) #fix
        terse.config(text="Current Theme: %s, %i %s" % (newTheme.theme.title, newTheme.size, newTheme.family))
        newTheme.apply([colorsHeader, fontSizeHeader, fontHeader, saveButton, cancelButton])
        for oo in r:
            newTheme.apply(oo)
        for oo in l:
            newTheme.apply(oo)

    r = [] #list of all radiobuttons
    l = [] #list of all accompanying labels

    colorsVar = StringVar(value=newTheme.theme.title)
    colorsOptions = [oo.title for oo in themes]
    colorsHeader = newTheme.apply(SelectLabel(midFrame, text="Color Theme:"))
    colorsHeader.grid(row=0, column=1, columnspan=1)

    for ii in range(len(colorsOptions)):
        r.append(newTheme.apply(Radiobutton(midFrame, variable=colorsVar, value=colorsOptions[ii], command=refresh)))
        l.append(newTheme.apply(SelectLabel(midFrame, text=colorsOptions[ii])))

        r[-1].grid(row=ii+1, column=0)
        l[-1].grid(row=ii+1, column=1)

    fontSizeVar = IntVar(value=newTheme.size)
    fontSizeHeader = newTheme.apply(SelectLabel(midFrame, text="Text Size:"))
    fontSizeHeader.grid(row=0, column=5, columnspan=1)

    for ii in range(len(sizes)):
        r.append(newTheme.apply(Radiobutton(midFrame, variable=fontSizeVar, value=sizes[ii], command=refresh)))
        l.append(newTheme.apply(SelectLabel(midFrame, text=str(sizes[ii]))))

        r[-1].grid(row=ii+1, column=4)
        l[-1].grid(row=ii+1, column=5)

    fontVar = StringVar(value=newTheme.family)
    fontHeader = newTheme.apply(SelectLabel(midFrame, text="Font Family:"))
    fontHeader.grid(row=0, column=3, columnspan=1)

    for ii in range(len(families)):
        r.append(newTheme.apply(Radiobutton(midFrame, variable=fontVar, value=families[ii], command=refresh)))
        l.append(newTheme.apply(SelectLabel(midFrame, text=families[ii])))

        r[-1].grid(row=ii+1, column=2)
        l[-1].grid(row=ii+1, column=3)


    def save():
        global T
        T = newTheme
        update()
        tl.destroy()

    #save button
    saveButton = newTheme(Button(botFrame, text="Save", command=save))
    saveButton.grid(row=0, column=0, padx=5, pady=5)

    #cancel button
    cancelButton = newTheme(Button(botFrame, text="Cancel", command=tl.destroy))
    cancelButton.grid(row=0, column=3, padx=5, pady=5)

    #set min window size
    tl.update_idletasks()
    tl.minsize(width=max(tl.winfo_reqwidth(),300), height=max(tl.winfo_reqheight(),200))

#build window block

#declaring dataFrame, which will hold all test widgets
dataFrame = LabelFrame(root, bd=0)
dataFrame.pack(side=TOP)

#Version label in the far right, on a window-spanning relief bar
#the relief also contains a hint message on the left side of the window
ver = Frame(root, bd=1, relief=SUNKEN)
hint = Label(ver, text = '')
hint.pack(side=LEFT)
verText = Label(ver, text="version " + version)
verText.pack(side=RIGHT)
ver.pack(side=BOTTOM, fill='x')

#build the windows-style menubar with multiple cascades
menubar = Menu(root)

fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label="Change Server Address", command=connect)
fileMenu.add_command(label="Write to File", command=writeToFile)
fileMenu.add_command(label="Exit", command=exitProgram)
menubar.add_cascade(label="File", menu=fileMenu)

viewMenu = Menu(menubar, tearoff=0)
viewMenu.add_command(label="Select Stations", command=changeView)
viewMenu.add_command(label="Clear all Stations", command=removeAllStations)
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
    T.apply([root, dataFrame, ver, fileMenu, viewMenu])
    verText.config(bg=T.theme.bg, fg=T.theme.fg, font=(T.family, T.size-2, "italic"))
    hint.config(bg=T.theme.bg, fg=T.theme.fg, font=(T.family, T.size-2))

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

    root.update_idletasks()
    root.geometry(str(max(root.winfo_reqwidth(),400))+'x'+str(max(root.winfo_reqheight(),300)))
    root.minsize(width=max(root.winfo_reqwidth(),400), height=max(root.winfo_reqheight(),300))

    
class Polling:
    def __init__(self):
        self.currTestPoll = 0
        self.running = True

    #main loop for recieving checking up and recieving from PLCs and continuing the GUI
    def mainloop(self):
        #if the loop encounters an error while parsing, it will mark the test as offline and proceed to poll the next test
        while(self.running): 
            if self.currTestPoll < len(tests):
                try:
                    get = requests.get(main_url+"station/"+tests[self.currTestPoll].url)
                    tests[self.currTestPoll].testNum = get.json()['number']
                    tests[self.currTestPoll].name = get.json()['title']
                    tests[self.currTestPoll].serial = get.json()['subtitle']
                    tests[self.currTestPoll].status = get.json()['status']
                    tests[self.currTestPoll].setData(get.json()['data'])
                    tests[self.currTestPoll].setControls(get.json()['controls'])
                    tests[self.currTestPoll].setOnline()

                except Exception as e:
                    tests[self.currTestPoll].setOffline()
                else:
                    tests[self.currTestPoll].setOnline()
                self.currTestPoll += 1
            if self.currTestPoll >= len(tests): #reset poll index to zero
                self.currTestPoll = 0

            sleep(pollPeriod)

    def stop(self):
        self.running = False

#main 
if __name__ == "__main__":
    #startup configuration block

    #add all themes from themes configuration file
    try:
        themefile = json.load(open("themes.json"))
        #expects a list of JSON objects with attributes that can be used to initialize Theme objects
        for kwargs in themefile:
            themes.append(tkTheme.Theme(**kwargs))

    except Exception as e:
        messagebox.showerror("Power Tools Test Viewer", "Problem encountered while loading from themes file", parent=root.focus_get())
    finally:
        if len(themes) == 0:
            themes.append(T.theme) #default theme

    #add all font options from font configuration file
    try:
        fontsfile = json.load(open("fonts.json"))
        #expects a list of font family names
        if "families" in fontsfile:
            if isinstance(fontsfile["families"], list):
                families.extend([oo for oo in fontsfile["families"] if oo in tkinter.font.families()])

        #expects a list of integer sizes
        if "sizes" in fontsfile:
            if isinstance(fontsfile["sizes"], list):
                sizes.extend([oo for oo in fontsfile["sizes"] if isinstance(oo, int)])

    except Exception as e:
        raise
        messagebox.showerror("Power Tools Test Viewer", "Problem encountered while loading from fonts file", parent=root.focus_get())
    finally:
        if len(families) == 0:
            families.append(T.family) #default font family
        if len(sizes) == 0:
            sizes.append(T.size) #default font size

    #configure on start up from config file
    try:
        conf = json.load(open("config.json"))

        #sets the main url on startup.  "url" accepts a string value, which becomes the main url
        if "url" in conf:
            if isinstance(conf['url'], str):
                main_url = conf['url']

        #determines whether the program attempts to add all the stations from the server on startup.  "addAll" accepts a boolean value.
        #If true, the program will attempt to contact the server and add all station
        if "addAll" in conf:
            if isinstance(conf['addAll'], bool):
                if conf['addAll']:
                    try:
                        get = requests.get(main_url + 'index')
                        for ii in range(len(get.json())):
                            tests.append(Test(get.json()[ii]['url'], get.json()[ii]['number'], get.json()[ii]['title'], get.json()[ii]['subtitle']))
                    except Exception as e:
                        pass

        #sets the display theme on startup.  "theme" accepts a string value.  If the value matches the name of a loaded theme, that theme will be selected, otherwise it will select the first loaded theme
        if "theme" in conf:
            if isinstance(conf['theme'], str):
                T.set(theme=next((oo for oo in themes if oo.title == conf['theme']), themes[0]))

        #sets the font family on startup.  "fontFamily" accepts a string value.  If the value is the name of a tkinter supported font, that font will be selected
        if "fontFamily" in conf:
            if conf["fontFamily"] in tkinter.font.families():
                T.set(family=conf["fontFamily"])

        #sets the font size on startup.  "fontSize" accepts an integer value to use as the size of the font
        if "fontSize" in conf:
            if isinstance(conf["fontSize"], int):
                T.set(size=conf["fontSize"])

    except Exception as e:
        messagebox.showerror("Power Tools Test Viewer", "Problem encountered while loading from config file", parent=root.focus_get())

    #draw screen for the first time
    update()
        
    poll = Polling()

    #list of all threads
    threads = []
    threads.append(threading.Thread(target=poll.mainloop))
    for oo in threads:
        oo.start()
    

    root.mainloop()
