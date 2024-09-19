from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

import customtkinter # type: ignore
import matcher
import settings
import os
import jotform_api

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = Tk()

def openSettingsWindow(*args):
    # Toplevel object which will 
    # be treated as a new window
    settingsWindow = Toplevel(root)

    settingsWindow.title("Settings")
    appWidth, appHeight = 480, 150
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
    appWidth, appHeight = 1090, 710
    root.geometry(f"{appWidth}x{appHeight}")
    root.resizable(False,False)

    # formId label
    root.formIdLabel = customtkinter.CTkLabel(root, text="Select Form: ")
    root.formIdLabel.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    def combobox_Changed(event):
        updateEventDateInput(root.formId_comboBox.get(), root)

    # form selection combo box
    if currentUser != False:
        values = matcher.getListOfUserForms()
        root.formId_comboBox = customtkinter.CTkComboBox(root, values=values, width=250, state="readonly", command=combobox_Changed)
    else:
        root.formId_comboBox = customtkinter.CTkComboBox(root, values=[], width=605, state="readonly")
    root.formId_comboBox.grid(row=0, column=1, columnspan=1, padx=20, pady=20, sticky="ew")

    # results text box
    root.resultsTextBox = customtkinter.CTkTextbox(root, width=920, height=495)
    root.resultsTextBox.grid(row=1, column=0, rowspan=3, columnspan=3, padx=20, pady=20, sticky="w")
    root.resultsTextBox.configure(state="disabled")

    # status info text box
    root.statusInfoTextBox = customtkinter.CTkTextbox(root, width=920, height=150)
    root.statusInfoTextBox.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
    root.statusInfoTextBox.configure(state="disabled")

    if currentUser != False:
        updateStatusBox(root.statusInfoTextBox, "User found! (" + currentUser["username"] + ")")
    else:
        updateStatusBox(root.statusInfoTextBox, "No account found for API key!\nPlease go to settings and enter a new API key.")

    # process button
    root.submitButton = customtkinter.CTkButton(root, text="Submit", command=lambda: processButton_Clicked(root))
    root.submitButton.grid(row=0, column=4, padx=20, pady=20, sticky="s")

    # settings button
    # TODO add license to settings
    root.settingsButton = customtkinter.CTkButton(root, text="Settings", fg_color="darkgray", text_color="black", hover_color="gray", command=openSettingsWindow)
    root.settingsButton.grid(row=1, column=4, padx=20, pady=20, sticky="n")

    # checkbox for including preference lists
    check_var = StringVar()
    root.preferenceListCheckbox = customtkinter.CTkCheckBox(root, text="Preference Lists?", variable=check_var, onvalue="on", offvalue="off")
    root.preferenceListCheckbox.grid(row=4, column=4, padx=20, pady=20, sticky="nw")

    # print button
    root.saveButton = customtkinter.CTkButton(root, text="Save Output", fg_color="darkgray", text_color="black", hover_color="gray", command=lambda: saveButton_Clicked(root))
    root.saveButton.grid(row=4, column=4, padx=20, pady=20, sticky="s")
    root.saveButton.configure(state="disabled")

    root.eventDate_comboBox = customtkinter.CTkComboBox(root, values='', width=8, state="readonly")

    root.formId_comboBox.focus()

    for child in root.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

# click events
def processButton_Clicked(root):
    # get form id
    formid = ""

    try:
        formid = matcher.getFormIdBasedOnFormTitle(root.formId_comboBox.get())
    except:
        processErrorMessage("ERROR 103: Form not found", root)
        return
    
    # get data from jotform
    data = jotform_api.JotformAPI.getJotformData(formid)
    
    # clear textbox
    updateTextBox(root.resultsTextBox, "")

    # check if form is valid format
    valid = matcher.checkFormValidity(data)

    if (valid):
        updateStatusBox(root.statusInfoTextBox, "Form valid!")
    else:
        processErrorMessage("ERROR 102: Invalid form", root)
        return

    # check if form has event date, if so then we will order the submissions by the event date, if not then we will continue as is
    hasDates = matcher.checkIfFormHasEventDate(data)

    # get response
    if (hasDates):
        eventDate = root.eventDate_comboBox.get()
        response = matcher.getMatches(data, eventDate)
    else:
        response = matcher.getMatches(data, "")

    # if response string has errors, handle those:
    if "error" in response[0].casefold():
        processErrorMessage(response[0], root)
        return
    
    # output response to text box
    updateTextBox(root.resultsTextBox, response[0])
    if (response[0] != ""):
        updateStatusBox(root.statusInfoTextBox, "Matches retrieved!")

    root.saveButton.configure(state="enabled")

def updateButton_Clicked(apikey, label):
    print(apikey)
    updatedBool = settings.updateAPIKey(apikey)
    if updatedBool == True:
        label.configure(text="API Key Updated! Please restart application.")
    else:
        label.configure(text="API Key field cannot be blank!")
 
def saveButton_Clicked(root):
    try:
        formid = matcher.getFormIdBasedOnFormTitle(root.formId_comboBox.get())
    except:
        processErrorMessage("ERROR 103: Form not found", root)
        return
    
    data = jotform_api.JotformAPI.getJotformData(formid)

    # check if form has event date, if so then we will order the submissions by the event date, if not then we will continue as is
    hasDates = matcher.checkIfFormHasEventDate(data)

    eventDate = ""
    if (hasDates):
        eventDate = root.eventDate_comboBox.get()

    # get list of matches with formid
    response = matcher.getMatches(data, eventDate) # response[0] = string, response[1] is matches dict

    outputStr = matcher.getOutputStringForFileSave(root.preferenceListCheckbox.get(), response, eventDate)
    saveFile(root.statusInfoTextBox, outputStr)


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

def saveFile(statusBox, outputStr):
    cwd = os.getcwd()
    files = [ 
             ('Text Document', '*.txt')
             ]
    file = filedialog.asksaveasfile(initialdir=cwd, defaultextension=files, filetypes=files)
    f = open(file.name, "w")
    f.write(outputStr)
    f.close()
    updateStatusBox(statusBox, "Outputted details to file: '{}'.".format(file.name))

def updateEventDateInput(formTitle, root): 
    # check if form has event date
    formid = ""

    try:
        formid = matcher.getFormIdBasedOnFormTitle(formTitle)
    except:
        updateStatusBox(root.statusInfoTextBox, "Could not find form with that title.")
        return
    
    # get jotform data
    data = jotform_api.JotformAPI.getJotformData(formid)
    
    hasDates = matcher.checkIfFormHasEventDate(data)

    if (hasDates):
        # root.submitButton.configure(state="enabled") # enable submission button
        eventDates = matcher.getEventDatesFromQuestions(data)
        root.eventDate_comboBox.configure(values=eventDates)
        root.eventDate_comboBox.grid(row=0, column=2, padx=5, pady=5, sticky="ew") # place combo box
        root.eventDate_comboBox.set(eventDates[0]) # set default value
    else:
        # root.submitButton.configure(state="disabled") # disable submission button
        root.eventDate_comboBox.grid_forget() # hide combo box
        root.eventDate_comboBox.set("")

def processErrorMessage(error, root):
    error_code = error.split(":")[0]

    if ("101") in error_code:
        updateStatusBox(root.statusInfoTextBox, "ERROR: Submission groups are not equal.")
    elif ("102") in error_code:
        updateStatusBox(root.statusInfoTextBox, "ERROR: Invalid form, please choose a form with the correct type of inputs (Control Matrix with Agree or Disagree columns).")
    elif ("103") in error_code:
        updateStatusBox(root.statusInfoTextBox, "ERROR: Could not find form with that title.")