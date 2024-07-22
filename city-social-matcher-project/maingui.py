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
        root.formId_comboBox = customtkinter.CTkComboBox(root, values=values, width=400, state="readonly")
    else:
        root.formId_comboBox = customtkinter.CTkComboBox(root, values=[], width=400, state="readonly")
    root.formId_comboBox.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

    # results text box
    root.resultsTextBox = customtkinter.CTkTextbox(root, width=520, height=280)
    root.resultsTextBox.grid(row=1, column=0, rowspan=3, columnspan=3, padx=20, pady=20, sticky="w")
    root.resultsTextBox.configure(state="disabled")

    # status info text box
    root.statusInfoTextBox = customtkinter.CTkTextbox(root, width=520, height=150)
    root.statusInfoTextBox.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
    root.statusInfoTextBox.configure(state="disabled")

    if currentUser != False:
        updateStatusBox(root.statusInfoTextBox, "User found! (" + currentUser["username"] + ")")
    else:
        updateStatusBox(root.statusInfoTextBox, "No account found for API key!\nPlease go to settings and enter a new API key.")
    
    # create paramters for methods to access
    parameters = [root]

    # process button
    root.submitButton = customtkinter.CTkButton(root, text="Submit", command=lambda: processButton_Clicked(root))
    root.submitButton.grid(row=0, column=4, padx=20, pady=20, sticky="s")

    # settings button
    root.settingsButton = customtkinter.CTkButton(root, text="Settings", fg_color="darkgray", text_color="black", hover_color="gray", command=openSettingsWindow)
    root.settingsButton.grid(row=1, column=4, padx=20, pady=20, sticky="n")

    # help button
    root.infoButton = customtkinter.CTkButton(root, text="Print Matches Details", fg_color="darkgray", text_color="black", hover_color="gray", command=lambda: infoButton_Clicked(root))
    root.infoButton.grid(row=4, column=4, padx=20, pady=20, sticky="s")
    root.infoButton.configure(state="disabled")

    root.formId_comboBox.focus()

    for child in root.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

# click events
def processButton_Clicked(arg):
    # set attributes
    root = arg
    comboBox = root.formId_comboBox
    textbox = root.resultsTextBox
    statusBox = root.statusInfoTextBox
    infoButton = root.infoButton

    # get list of matches with formid
    formid = matcher.getFormIdBasedOnFormTitle(comboBox.get())
    response = matcher.getMatches(formid)

    # update textbox and status box
    updateTextBox(textbox, response[0])
    updateStatusBox(statusBox, "Matches retrieved!")
    updateStatusBox(statusBox, "Outputted matches to file 'matches.txt'.")

    # enable info button
    infoButton.configure(state="enabled")

def updateButton_Clicked(apikey, label):
    print(apikey)
    updatedBool = settings.updateAPIKey(apikey)
    if updatedBool == True:
        label.configure(text="API Key Updated! Please restart application.")
    else:
        label.configure(text="API Key field cannot be blank!")

def infoButton_Clicked(arg):
    # set attributes
    root = arg
    comboBox = root.formId_comboBox
    statusBox = root.statusInfoTextBox

    # get list of matches with formid
    formid = matcher.getFormIdBasedOnFormTitle(comboBox.get())
    response = matcher.getMatches(formid)

    filename = "matches-details.txt"
    matcher.outputToFile(filename, response[1])
    updateStatusBox(statusBox, "Outputted details to file: '{}'.".format(filename))

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