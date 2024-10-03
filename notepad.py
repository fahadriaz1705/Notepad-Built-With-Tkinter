from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

filePath = NONE  # Global variable to store the file path

# Function to handle different menu actions
def menuMethods(label):
    global filePath

    # Code for File dropdown methods
    if(label == "New"):
        answer = messagebox.askyesno("Question","Do you want to save changes?")
        if(answer == True):
            menuMethods("Save As")
        else:
            screen.delete(1.0,END)
            screen.update()
    elif(label == "Save As"):
        print("this is code for save as")
        filePath = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filePath:
            with open(filePath,"w") as file:
                file.write(screen.get(1.0,END))
    elif( label == "Open"):
        print("this is code for open")
        filePathOpen = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filePathOpen:
            with open(filePathOpen,"r") as file:
                fileContent = file.read()
                screen.delete(1.0,END)
                screen.insert(1.0,fileContent)
                screen.update()
    elif( label == "Save"):
        if filePath != NONE:
            with open(filePath,"w") as file:
                file.write(screen.get(1.0,END))
        else:
            filePath = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            with open(filePath,"w") as file:
                file.write(screen.get(1.0,END))
    elif(label == "Exit"):
        answer = messagebox.askokcancel("Question","Do you want to exit Notepad?")
        if answer == True:
            exit()
        else:
            pass
    
    # Code for Edit dropdown methods
    elif( label == "Copy"):
        copiedText = screen.get(SEL_FIRST,SEL_LAST)
        screen.clipboard_clear()
        screen.clipboard_append(copiedText)
    elif(label == "Paste"):
        pasteText = screen.clipboard_get()
        screen.insert(INSERT,f" {pasteText}")
        screen.update()
    elif(label == "Cut"):
        cutText = screen.get(SEL_FIRST,SEL_LAST)
        screen.clipboard_clear()
        screen.clipboard_append(cutText)
        screen.delete(SEL_FIRST,SEL_LAST)
    elif(label == "Delete"):
        screen.delete(SEL_FIRST,SEL_LAST)
    elif(label == "Find"):
        findPopup()
    elif(label == "Replace"):
        replacePopup()
    elif(label == "Font"):
        fontWindow()

# Function to create a popup window for finding text
def findPopup():
    popUp = Toplevel(root)
    popUp.geometry("250x50")
    popUp.title("Find")
    popUp.transient(root)
    popUp.iconbitmap("notepad.ico")
    Label(popUp,text="Find What:",font="arial 8").grid(row=0,column=0,padx=5,pady=5)
    findVar = StringVar()
    findEntry = Entry(popUp,textvariable=findVar)
    findEntry.grid(row=0,column=1,padx=5,pady=5)
    Button(popUp,text="Find",bg="light green",font="arial 8",command= lambda: findWord(findVar.get())).grid(row=0,column=2,padx=5,pady=5)

# Function to create a popup window for replacing text
def replacePopup():
    replacePop = Toplevel(root)
    replacePop.geometry("300x100")
    replacePop.title("Replace")
    replacePop.iconbitmap("notepad.ico")
    Label(replacePop,text="Find:",font="arial 8").grid(row=0,column=0,padx=5,pady=5)
    wordVar = StringVar()
    wordEnt = Entry(replacePop,textvariable=wordVar,font="arial 8")
    wordEnt.grid(row=0,column=2,padx=5,pady=5)
    Label(replacePop,text="Replace:",font="arial 8").grid(row=1,column=0,padx=5,pady=5)
    replaceVar = StringVar()
    replaceEnt = Entry(replacePop,textvariable=replaceVar,font="arial 8")
    replaceEnt.grid(row=1,column=2,padx=5,pady=5)
    Button(replacePop,text="Replace",bg="light green",font="arial 8",command= lambda: replaceWord(wordEnt.get(),replaceEnt.get())).grid(row=2,column=1)

# Function to find and highlight text in the Text widget
def findWord(word):
    start_pos = "1.0"
    while True:
        pos = screen.search(word, start_pos, stopindex=END)
        if not pos:
            break
        end_pos = f"{pos}+{len(word)}c"
        screen.tag_add("found", pos, end_pos)
        start_pos = end_pos
    screen.tag_configure("found", background="yellow", foreground="black")

# Function to replace text in the Text widget
def replaceWord(word,replace):
    startPos = 1.0
    while True:
        pos = screen.search(word,startPos,stopindex=END)
        if pos:
            endPos = (f"{pos} + {len(word)}c")
            screen.delete(pos,endPos)
            screen.insert(pos,replace)
            startPos = (f"{pos} + {len(replace)}c")
        else:
            break

# Function to create a popup window for font selection
def fontWindow():
    fontPopup = Toplevel(root)
    fontPopup.geometry("300x250")
    fontPopup.minsize(300,250)
    fontPopup.title("Font")
    fontPopup.iconbitmap("notepad.ico")
    fonts = ["Arial","Roman","Courier","MS Serif","MS Sans Serif","Birch std","Chaparral Pro","Cooper Std Black","Charlemagne Std","Brush Script Std","Blackoak Std","Arial Baltic","Arial TUR","Vani","Gulim","Euphemia","Kartika"]
    Label(fontPopup,text="Fonts:",font="arial 8").grid(row=0,column=0,padx=0,pady=0,sticky="n")
    scroll = Scrollbar(fontPopup)
    scroll.grid(row=0,column=2,sticky="ns")
    fontList = Listbox(fontPopup,yscrollcommand=scroll.set)
    fontList.grid(row=0,column=1)
    scroll.config(command= fontList.yview)
    Label(fontPopup,text="Font Size:",font="arial 8").grid(row=1,column=0,padx=5,pady=5)
    fontVar = StringVar()
    sizeEnt = Entry(fontPopup,textvariable=fontVar,font="arial 8")
    sizeEnt.grid(row=1,column=1,padx=5,pady=5)
    for i,font in enumerate(fonts):
        fontList.insert(i,font)
    Button(fontPopup,text="Set Font",bg="light green",font="Arial 8",command= lambda: setFont(fontList.get(ACTIVE),sizeEnt.get())).grid(row=2,column=1)

# Function to set the selected font in the Text widget
def setFont(fontName,fontSize):
    screen.config(font=(fontName,fontSize))

root = Tk()
root.geometry("900x600")
root.minsize(400,300)
root.title("Notepad by Fahad Riaz")
root.iconbitmap("notepad.ico")

# Code for drop down main menu
mainMenu = Menu(root)
root.config(menu=mainMenu)

# Code for File menu
fileMenu = Menu(mainMenu,tearoff=0)
fileMenu.add_command(label="New",command= lambda: menuMethods("New"))
fileMenu.add_command(label="Open",command= lambda: menuMethods("Open"))
fileMenu.add_separator()
fileMenu.add_command(label="Save As",command=lambda: menuMethods("Save As"))
fileMenu.add_command(label="Save",command=lambda: menuMethods("Save"))
fileMenu.add_separator()
fileMenu.add_command(label="Exit",command=lambda: menuMethods("Exit"))
mainMenu.add_cascade(menu=fileMenu,label="File")

# Code for Edit menu
editMenu = Menu(mainMenu,tearoff=0)
editMenu.add_command(label="Copy",command=lambda: menuMethods("Copy"))
editMenu.add_command(label="Paste",command= lambda: menuMethods("Paste"))
editMenu.add_command(label="Cut",command= lambda: menuMethods("Cut"))
editMenu.add_command(label="Delete",command= lambda: menuMethods("Delete"))
editMenu.add_separator()
editMenu.add_command(label="Find",command= lambda: menuMethods("Find"))
editMenu.add_command(label="Replace",command= lambda: menuMethods("Replace"))
mainMenu.add_cascade(menu=editMenu,label="Edit")

# Code for Font menu
fontMenu = Menu(mainMenu,tearoff=0)
fontMenu.add_command(label="Font",command= lambda: menuMethods("Font"))
mainMenu.add_cascade(label="Format",menu=fontMenu)

# Code for scroll bar
scrollBar = Scrollbar(root)
scrollBar.grid(row=0,column=1,sticky="ns")

# Code for Text screen
screen = Text(root,font="arial 12",yscrollcommand=scrollBar.set)
screen.grid(row=0,column=0,sticky="nsew")
scrollBar.config(command= screen.yview)

# Configuring grid layout
root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(0,weight=1)

# Create a status bar at the bottom of the window
statusBar = Label(root, text="Ready", bd=1, relief=SUNKEN, anchor=W)
statusBar.grid(row=1, column=0, sticky="ew")

# Update the status bar when the text changes
def update_status_bar(event=None):
    statusBar.config(text="Characters: " + str(len(screen.get("1.0", "end-1c"))))

screen.bind("<KeyRelease>", update_status_bar)

root.mainloop()
