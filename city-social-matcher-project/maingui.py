from tkinter import *
from tkinter import ttk
from datetime import datetime

import customtkinter # type: ignore
import matcher
import settings

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = Tk()

def openSettingsWindow(*args):
    # Toplevel object which will 
    # be treated as a new window
    settingsWindow = Toplevel(root)

    settingsWindow.title("Settings")
    appWidth, appHeight = 480, 200
    settingsWindow.geometry(f"{appWidth}x{appHeight}")

    # apikey label
    settingsWindow.apikeyLabel = customtkinter.CTkLabel(settingsWindow, text="Jotform API Key", width=40)
    settingsWindow.apikeyLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # results label
    settingsWindow.resultsLabel = customtkinter.CTkLabel(settingsWindow, text="")
    settingsWindow.resultsLabel.grid(row=1, column=0, padx=0, pady=0, sticky="w", columnspan=2)

    # apikey entry
    apikey = StringVar()
    currentKey = settings.getAPIKey()
    print(currentKey)
    settingsWindow.apikeyEntry = customtkinter.CTkEntry(settingsWindow, placeholder_text="test", textvariable=apikey, width=200)
    settingsWindow.apikeyEntry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")

    # update apikey button
    settingsWindow.apikeyUpdateButton = customtkinter.CTkButton(settingsWindow, text="Update", command=lambda: updateButton_Clicked(apikey.get(), settingsWindow.resultsLabel))
    settingsWindow.apikeyUpdateButton.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    for child in settingsWindow.winfo_children():
        child.grid_configure(padx=5, pady=5)
    

def createMainWindow():
    currentUser = settings.checkCurrentUser()
    
    root.title("City Social Matcher")
    appWidth, appHeight = 680, 500
    root.geometry(f"{appWidth}x{appHeight}")
    root.resizable(False,False)

    # formId label
    root.formIdLabel = customtkinter.CTkLabel(root, text="Select Form: ")
    root.formIdLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

    # form selection combo box
    if currentUser != False:
        values = matcher.getListOfUserForms()
        formId_comboBox = customtkinter.CTkComboBox(root, values=values, width=400, state="readonly")
    else:
        formId_comboBox = customtkinter.CTkComboBox(root, values=[], width=400, state="readonly")
    formId_comboBox.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

    # results text box
    resultsTextBox = customtkinter.CTkTextbox(root, width=520, height=280)
    resultsTextBox.grid(row=1, column=0, rowspan=3, columnspan=3, padx=20, pady=20, sticky="w")
    resultsTextBox.configure(state="disabled")

    # status info text box
    statusInfoTextBox = customtkinter.CTkTextbox(root, width=520, height=150)
    statusInfoTextBox.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
    statusInfoTextBox.configure(state="disabled")

    if currentUser != False:
        updateStatusBox(statusInfoTextBox, "User found! (" + currentUser["username"] + ")")
    else:
        updateStatusBox(statusInfoTextBox, "No account found for API key!\nPlease go to settings and enter a new API key.")
    
    # create paramters for methods to access
    parameters = [formId_comboBox, resultsTextBox, statusInfoTextBox]

    # process button
    root.submitButton = customtkinter.CTkButton(root, text="Submit", command=lambda: processButton_Clicked(parameters))
    root.submitButton.grid(row=0, column=4, padx=20, pady=20, sticky="s")

    # settings button
    root.settingsButton = customtkinter.CTkButton(root, text="Settings", fg_color="darkgray", text_color="black", hover_color="gray", command=openSettingsWindow)
    root.settingsButton.grid(row=1, column=4, padx=20, pady=20, sticky="n")

    # help button
    root.helpButton = customtkinter.CTkButton(root, text="Help", fg_color="darkgray", text_color="black", hover_color="gray")
    root.helpButton.grid(row=4, column=4, padx=20, pady=20, sticky="s")

    formId_comboBox.focus()

    for child in root.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

# click events
def processButton_Clicked(parameters):
    # set attributes
    comboBox = parameters[0]
    textbox = parameters[1]
    statusBox = parameters[2]

    # get list of matches with formid
    formid = matcher.getFormIdBasedOnFormTitle(comboBox.get())
    matches = matcher.getMatches(formid)

    # update textbox and status box
    updateTextBox(textbox, matches)
    updateStatusBox(statusBox, "Matches retrieved!")

def updateButton_Clicked(apikey, label):
    print(apikey)
    updatedBool = settings.updateAPIKey(apikey)
    if updatedBool == True:
        label.configure(text="API Key Updated! Please restart application.")
    else:
        label.configure(text="API Key field cannot be blank!")

# helper methods
def clearTextBox(textbox):
    textbox.configure(state="normal")
    textbox.delete('1.0', END)
    textbox.configure(state="disabled")

def updateTextBox(textbox, content):
    clearTextBox(textbox)
    textbox.configure(state="normal")
    textbox.insert("insert", content)
    textbox.configure(state="disabled")

def updateStatusBox(statusBox, message):
    dt_string = datetime.now().strftime("%H:%M:%S") # mm/dd/YY H:M:S

    statusBox.configure(state="normal")
    statusBox.insert("insert", "(" + dt_string + ") " + message + "\n")
    statusBox.configure(state="disabled")