import tkinter as tk
from tkinter import Canvas, BOTH, Frame, Grid
from datetime import datetime, timedelta
from random import randint
from Meal import Meal
from CalendarDay import CalendarDay

class CalendarPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 

        #self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        # for column in range(7):
        #     Grid.columnconfigure(self, column, weight=1)

        # for row in range(2):
        #     Grid.rowconfigure(self, row, weight=1)

        # Get the date of the next Monday (today, if today is monday)
        dayInCurrentWeek = datetime.today()
        firstDayOfWeek = dayInCurrentWeek
        
        foundMonday = False
        while not foundMonday:
            if dayInCurrentWeek.weekday() == 0:
                foundMonday = True
                firstDayOfWeek = dayInCurrentWeek
            else:
                dayInCurrentWeek = dayInCurrentWeek + timedelta(days=1)

        fourteenDays = self.getDays(firstDayOfWeek)

        randomMeals = self.getRandomMeals()

        fourteenDaysWithMeals = self.assignMealsToDays(randomMeals, fourteenDays)
        
        self.drawCalendar(fourteenDaysWithMeals)

        #TODO: navigate back to menu page
        backToMainMenuButton = tk.Button(self, text="Back to menu", command = lambda: controller.show_page("MainMenuPage"))
        backToMainMenuButton.grid(row=2,column=6, ipadx=5, ipady=5, padx=5, pady=5, sticky="NSEW")

    def assignMealsToDays(self, meals, days):
        numDays = len(days)
        for x in range (numDays):
            days[x].meal = meals[x]

        return days

    def drawCalendar(self, daysToDraw):

        #cellWidth = 120
        #cellHeight = 110
        cellMargin = 5
        cellPadding = 5
        
        for row in range(2):
            for column in range(7):
                dayIndex = row + column
                day = daysToDraw[dayIndex]
                cellBackgroundColour = "white"
                if day.date.strftime("%a %d %b") == datetime.today().strftime("%a %d %b"):
                    cellBackgroundColour = "green"
                meal = day.meal
                cellText = day.date.strftime("%a %d %b") + "\n\n" + meal.name
                
                dayBoxFrame = Frame(self, highlightbackground="blue", highlightthickness=2, bd=0)
                
                showMealButton = tk.Button(dayBoxFrame, text=cellText, height=4, width=13, command=lambda buttonText=cellText: self.popup_meal(buttonText), bg=cellBackgroundColour, bd=0, relief=tk.FLAT)
                
                showMealButton.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=tk.YES)
                #showMealButton.config(borderwidth=2, highlightbackground = "red", highlightcolor= "red")
                #showMealButton.grid(row=row,column=column, ipadx=cellPadding, ipady=cellPadding, padx=cellMargin, pady=cellMargin)
                dayBoxFrame.grid(row=row, column=column, ipadx=cellPadding, ipady=cellPadding, padx=cellMargin, pady=cellMargin)

    def popup_meal(self, val):
        def closePopupWindow():
            popupWindow.grab_release()
            popupWindow.destroy()

        popupWindow = tk.Toplevel()
        popupWindow.wm_geometry("200x200")
        popupWindow.title("Meal Info")
        popupWindow.attributes ("-topmost", True)
        popupWindow.grab_set()
        lbl = tk.Label(popupWindow, text=val)
        lbl.grid()
        no_btn = tk.Button(popupWindow, text="Done", bg="light blue", fg="red", command=closePopupWindow, width=10)
        no_btn.grid()

    # Generate 14 days worth of random meals
    def getRandomMeals(self):
        # TODO: read meals from a file, so that new meals can be added by the user in the app.
        meals = [Meal("meal_1"), Meal("meal_2"), Meal("meal_3"), Meal("meal_4"), Meal("meal_5"), Meal("meal_6"), Meal("meal_7"), Meal("meal_8"), Meal("meal_9"), Meal("meal_10"), Meal("meal_11"), Meal("meal_12"), Meal("meal_13"), Meal("meal_14"), Meal("meal_15"), Meal("meal_16"), Meal("meal_17"), Meal("meal_18"), Meal("meal_19"), Meal("meal_20"), Meal("meal_21"), Meal("meal_22"), Meal("meal_23"), Meal("meal_24"), Meal("meal_25")]

        randomIndexes = []

        foundEnoughRandomIndexes = False
        while not foundEnoughRandomIndexes:
            value = randint(0, 24)
            if value not in randomIndexes:
                randomIndexes.append(value)
            if len(randomIndexes) == 14:
                foundEnoughRandomIndexes = True

        chosenMeals = []

        for index in randomIndexes:
            chosenMeals.append(meals[index])

        return chosenMeals

    def getDays(self, firstDayOfWeek):
        days = [CalendarDay(firstDayOfWeek, None)]

        dayOfWeek = firstDayOfWeek
        for x in range (13):
            dayOfWeek = dayOfWeek + timedelta(days=1)
            days.append(CalendarDay(dayOfWeek, None))

        return days