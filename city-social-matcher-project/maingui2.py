from tkinter import *
from tkinter import ttk

import customtkinter # type: ignore
import matcher
import settings

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = Tk()
# root.withdraw()

class AppGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("City Social Matcher")
        appWidth, appHeight = 600, 500
        self.geometry(f"{appWidth}x{appHeight}")

        # formId label
        self.formIdLabel = customtkinter.CTkLabel(self, text="Jotform Form ID: ")
        self.formIdLabel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # formId entry
        formid = StringVar()
        self.formIdEntry = customtkinter.CTkEntry(self, placeholder_text="4872837462", width=220, textvariable=formid)
        self.formIdEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="w")

        # results text box
        self.resultsTextBox = customtkinter.CTkTextbox(master=self, width=340)
        self.resultsTextBox.grid(row=1, column=0, rowspan=3, columnspan=3, padx=20, pady=20, sticky="w")
        self.resultsTextBox.configure(state="disabled")

        # form info text box
        self.formInfoTextBox = customtkinter.CTkTextbox(master=self, width=340, height=130)
        self.formInfoTextBox.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
        self.formInfoTextBox.configure(state="disabled")

        # process button
        self.submitButton = customtkinter.CTkButton(self, text="Submit", command=lambda: self.updateResultsTextBox())
        self.submitButton.grid(row=0, column=4, padx=20, pady=20, sticky="ew")

        # settings button
        self.settingsButton = customtkinter.CTkButton(self, text="Settings", fg_color="darkgray", text_color="black", hover_color="gray", command=openSettingsWindow)
        self.settingsButton.grid(row=1, column=4, padx=20, pady=20, sticky="n")

        # connect to jotform button
        self.submitButton = customtkinter.CTkButton(self, text="Get Submissions", command=lambda: self.updateFormInfoTextBox(formid.get()))
        self.submitButton.grid(row=2, column=4, padx=20, pady=20, sticky="n")

        # help button
        self.helpButton = customtkinter.CTkButton(self, text="Help", fg_color="darkgray", text_color="black", hover_color="gray")
        self.helpButton.grid(row=4, column=4, padx=20, pady=20, sticky="s")

    def updateResultsTextBox(self):
        self.resultsTextBox.configure(state="normal")
        self.resultsTextBox.insert("insert", "hello")
        self.resultsTextBox.configure(state="disabled")

    def updateFormInfoTextBox(self, formid):
        self.formInfoTextBox.configure(state="normal")
        self.formInfoTextBox.insert("insert", "helllo")
        self.formInfoTextBox.configure(state="disabled")

def createMainWindow3():
    app = AppGUI()
    app.mainloop()