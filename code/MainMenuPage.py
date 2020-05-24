import tkinter as tk
from CalendarPage import CalendarPage

class MainMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # create the stuff we want to show on the menu page
        label = tk.Label(self, text='Meal Planner')

        # When this button is clicked, tell the controller to show the 'Meal Planner' page.
        planMealsButton = tk.Button(self, text='Plan some meals!', command=lambda : controller.show_page(CalendarPage))

        # ley the stuff out where we want it to be ont he menu page
        label.pack(pady=10, padx=10)
        planMealsButton.pack()