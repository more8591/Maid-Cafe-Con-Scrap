import customtkinter
from test import eventList

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1280x720")

def button_function():
    print("button pressed")

def getEventList():
    x = 0
    y = 0
    for i in range(0, len(eventList)):
        x = 0.1 + x
        y = 0.1 + y
        customtkinter.CTkLabel(master=app, text=eventList[i]['event name'], fg_color="transparent").place(relx=x, rely=y, anchor=customtkinter.S)


# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="CTkButton", command=getEventList)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


app.mainloop()