from tkinter import *
from tkinter import ttk

import matcher

def createMainWindow(*args):

    # set up main application window
    root = Tk()
    root.title("City Social Matcher")

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
    ttk.Label(mainframe, text="Jotform Form ID: ").grid(column=1, row=1)

    # output
    # matches
    matches = StringVar()
    ttk.Label(mainframe, textvariable=matches).grid(column=2, row=2, sticky=(W, E))

    # buttons
    # process button
    ttk.Button(mainframe, text="Get Matches", command=lambda: matcher.getMatches()).grid(column=3, row=3, sticky=W)

    ttk.Button(mainframe, text="Get Responses", command=lambda: matcher.getSubmissions(formId.get())).grid(column=2, row=3, sticky=(W, E))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    formId_entry.focus()
    root.bind("<Return>", lambda: matcher.getMatches())

    root.mainloop()

# createMainWindow()