from tkinter import *
from tkinter import ttk

import customtkinter # type: ignore
import matcher
import settings

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

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

    settingsWindow.title("Settings")
    appWidth, appHeight = 420, 300
    settingsWindow.geometry(f"{appWidth}x{appHeight}")

    # apikey label
    settingsWindow.apikeyLabel = customtkinter.CTkLabel(settingsWindow, text="Jotform API Key")
    settingsWindow.apikeyLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # apikey entry
    apikey = StringVar()
    settingsWindow.apikeyEntry = customtkinter.CTkEntry(settingsWindow, placeholder_text=lambda: settings.getAPIKey(), textvariable=apikey)
    settingsWindow.apikeyEntry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")

    # update apikey button
    settingsWindow.apikeyUpdateButton = customtkinter.CTkButton(settingsWindow, text="Update", command=lambda: settings.updateAPIKey(apikey.get()))
    settingsWindow.apikeyUpdateButton.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    for child in settingsWindow.winfo_children():
        child.grid_configure(padx=5, pady=5)
    
# createMainWindow()

def createMainWindow2():
    root.title("City Social Matcher")
    appWidth, appHeight = 680, 500
    root.geometry(f"{appWidth}x{appHeight}")
    root.resizable(False,False)

    # formId label
    root.formIdLabel = customtkinter.CTkLabel(root, text="Jotform Form ID: ")
    root.formIdLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

    # formId entry
    formid = StringVar()
    # formIdEntry = customtkinter.CTkEntry(root, placeholder_text="4872837462", width=220, textvariable=formid)
    # formIdEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="w")

    # form selection combo box
    values = matcher.getListOfUserForms()
    formId_comboBox = customtkinter.CTkComboBox(root, values=values, width=400, state="readonly")
    formId_comboBox.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

    # results text box
    resultsTextBox = customtkinter.CTkTextbox(root, width=520, height=280)
    resultsTextBox.grid(row=1, column=0, rowspan=3, columnspan=3, padx=20, pady=20, sticky="w")
    resultsTextBox.configure(state="disabled")

    # form info text box
    formInfoTextBox = customtkinter.CTkTextbox(root, width=520, height=150)
    formInfoTextBox.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
    formInfoTextBox.configure(state="disabled")
    
    # create paramters for methods to access
    parameters = [formId_comboBox, resultsTextBox, formInfoTextBox]

    # process button
    root.submitButton = customtkinter.CTkButton(root, text="Submit", command=lambda: processButton_Clicked(parameters))
    root.submitButton.grid(row=0, column=4, padx=20, pady=20, sticky="s")

    # settings button
    root.settingsButton = customtkinter.CTkButton(root, text="Settings", fg_color="darkgray", text_color="black", hover_color="gray", command=openSettingsWindow)
    root.settingsButton.grid(row=1, column=4, padx=20, pady=20, sticky="n")

    # # connect to jotform button
    # root.getSubmissions = customtkinter.CTkButton(root, text="Get Submissions", command=lambda: getSubmissionsButton_Clicked(parameters))
    # root.getSubmissions.grid(row=2, column=4, padx=20, pady=20, sticky="n")

    # help button
    root.helpButton = customtkinter.CTkButton(root, text="Help", fg_color="darkgray", text_color="black", hover_color="gray")
    root.helpButton.grid(row=4, column=4, padx=20, pady=20, sticky="s")

    formId_comboBox.focus()

    for child in root.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

def processButton_Clicked(parameters):
    textbox = parameters[1]
    # formid = parameters[0].get()
    textbox.configure(state="normal")
    comboBox = parameters[0]
    formid = matcher.getFormIdBasedOnFormTitle(comboBox.get())
    matches = matcher.getMatches(formid)
    print(matches)
    textbox.insert("insert", matches)
    textbox.configure(state="disabled")

# def getSubmissionsButton_Clicked(parameters):
#     textbox = parameters[2]
#     formid = parameters[0].get()
#     textbox.configure(state="normal")
#     submissions = matcher.getDataFromSubmissions(formid)
#     textbox.insert("insert", submissions)
#     textbox.configure(state="disabled")