from tkinter import *
from tkinter import ttk

import customtkinter
import matcher
import settings

root = Tk()

def createMainWindow(*args):

    # set up main application window
    root.title("City Social Matcher")
    # root.geometry("500x500")

    # set up content frame
    mainframe = ttk.Frame(root, padding="6 6 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # input
    # formId
    formId = StringVar()
    formId_entry = ttk.Entry(mainframe, width=20, textvariable=formId)
    formId_entry.grid(column=2, row=1, sticky=(W, E))
    customtkinter.CTkLabel(mainframe, text="Jotform Form ID: ").grid(column=1, row=1)

    # output
    # matches
    matches = StringVar()
    ttk.Label(mainframe, textvariable=matches).grid(column=2, row=2, sticky=(W, E))

    # buttons
    # process button
    customtkinter.CTkButton(mainframe, text="Get Matches", command=lambda: matcher.getMatches()).grid(column=3, row=1, sticky=W)

    customtkinter.CTkButton(mainframe, text="(test) Get Responses", command=lambda: matcher.getSubmissions(formId.get())).grid(column=1, row=3, sticky=(W, E))

    customtkinter.CTkButton(mainframe, text="Settings", command=openSettingsWindow).grid(column=3, row=3, sticky=(W, E))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    formId_entry.focus()
    root.bind("<Return>", lambda: matcher.getMatches())

    root.mainloop()

def openSettingsWindow(*args):
     
    # Toplevel object which will 
    # be treated as a new window
    settingsWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    settingsWindow.title("Settings")
 
    # # sets the geometry of toplevel
    # settingsWindow.geometry("300x300")

    # set up content frame
    # settingsFrame = ttk.Frame(root, padding="6 6 12 12")
    # settingsFrame.grid(column=0, row=0, sticky=(N, S, E, W))
    # root.columnconfigure(0, weight=1)
    # root.rowconfigure(0, weight=1)
 
    # A Label widget to show in toplevel
    # Label(settingsWindow, 
    #       text ="This is a new window").pack()

    for child in settingsWindow.winfo_children():
        child.grid_configure(padx=5, pady=5)
    
    apikey = StringVar()
    apikey_entry = ttk.Entry(settingsWindow, width=20, textvariable=apikey)
    apikey_entry.grid(column=1, row=1, sticky=(W, E))
    ttk.Button(settingsWindow, text="Update API Key", command=lambda: settings.updateAPIKey(apikey.get())).grid(column=3, row=1, sticky=W)

# createMainWindow()