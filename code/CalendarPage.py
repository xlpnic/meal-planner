import tkinter as tk
from tkinter import Canvas, BOTH, Frame, Grid
from datetime import datetime, timedelta
from random import randint
from Meal import Meal
from CalendarDay import CalendarDay

class CalendarPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 

        firstDayOfWeek = self.getNextMondayDate()

        fourteenDays = self.getDays(firstDayOfWeek)

        fourteenRandomMeals = self.getRandomMeals()

        fourteenDaysWithMeals = self.assignMealsToDays(fourteenRandomMeals, fourteenDays)
        
        self.drawCalendar(fourteenDaysWithMeals)

        backToMainMenuButton = tk.Button(self, text="Back to menu", command = lambda: controller.show_page("MainMenuPage"))
        backToMainMenuButton.grid(row=2,column=6, ipadx=5, ipady=5, padx=5, pady=5, sticky="NSEW")
    
    def getNextMondayDate(self):
        dayInCurrentWeek = datetime.today()
        firstDayOfWeek = dayInCurrentWeek
        
        foundMonday = False
        while not foundMonday:
            if dayInCurrentWeek.weekday() == 0:
                foundMonday = True
                firstDayOfWeek = dayInCurrentWeek
            else:
                dayInCurrentWeek = dayInCurrentWeek + timedelta(days=1)
        return firstDayOfWeek

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
                
                showMealButton = tk.Button(dayBoxFrame, text=cellText, height=4, width=13, command=lambda chosenMeal=meal: self.popup_meal(chosenMeal), bg=cellBackgroundColour, bd=0, relief=tk.FLAT)
                
                showMealButton.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=tk.YES)
                #showMealButton.config(borderwidth=2, highlightbackground = "red", highlightcolor= "red")
                #showMealButton.grid(row=row,column=column, ipadx=cellPadding, ipady=cellPadding, padx=cellMargin, pady=cellMargin)
                dayBoxFrame.grid(row=row, column=column, ipadx=cellPadding, ipady=cellPadding, padx=cellMargin, pady=cellMargin)

    def popup_meal(self, chosenMeal):
        def closePopupWindow():
            popupWindow.grab_release()
            popupWindow.destroy()

        #TODO: instead of getting the centre of the screen, get the centre of the parent window.
        w=400
        h=200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (w/2)
        y = (screen_height/2) - (h/2)

        popupWindow = tk.Toplevel()
        popupWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
        popupWindow.title("Meal Info")
        popupWindow.attributes ("-topmost", True)
        popupWindow.overrideredirect(True)
        popupWindow.grab_set()

        popupWindow.columnconfigure(0, weight=1)
        popupWindow.rowconfigure(0, weight=1)

        popupWindowFrame = Frame(popupWindow, highlightbackground="red", highlightthickness=2, bd=0, bg="blue")
        lbl = tk.Label(popupWindowFrame, text=chosenMeal.name)
        lbl.pack()
        no_btn = tk.Button(popupWindowFrame, text="Done", bg="light blue", fg="red", command=closePopupWindow, width=10)
        no_btn.pack()
        popupWindowFrame.grid(column=0, row=0, ipadx=10, ipady=10, sticky="NSEW")

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