import tkinter as tk
from tkinter import Canvas, BOTH, Frame, Grid
from datetime import datetime, timedelta
from random import randint
from Meal import Meal
from Ingredient import Ingredient
from CalendarDay import CalendarDay
from MethodStep import MethodStep
import json

class CalendarPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 

        firstDayOfWeek = self.getNextMondayDate()

        fourteenDays = self.getDays(firstDayOfWeek)

        availableMeals = self.loadMeals()

        randomlyChosenMeals = self.getRandomMeals(availableMeals)

        fourteenDaysWithMeals = self.assignMealsToDays(randomlyChosenMeals, fourteenDays)
        
        self.drawCalendar(fourteenDaysWithMeals)

        backToMainMenuButton = tk.Button(self, text="Back to menu", command = lambda: controller.show_page("MainMenuPage"))
        backToMainMenuButton.grid(row=2,column=6, ipadx=5, ipady=5, padx=5, pady=5, sticky="NSEW")

    def loadMeals(self):
        # read file
        with open('demo-data.json', 'r') as demoDataFile:
            demoData=demoDataFile.read()

        # parse file
        demoDataJsonObject = json.loads(demoData)

        print("length: " + str(len(demoDataJsonObject)))

        meals = []

        for mealData in demoDataJsonObject :
            ingredientsObject = mealData['ingredients']
            ingredients = []
            for ingredientData in ingredientsObject:
                newIngredient = Ingredient(ingredientData['name'], ingredientData['quantity'], ingredientData['units'], ingredientData['size'])
                ingredients.append(newIngredient)
            methodStepsObject = mealData['method']
            methodSteps = []
            for methodStepData in methodStepsObject:
                newMethodStep = MethodStep(methodStepData['stepNumber'], methodStepData['stepDescription'])
                methodSteps.append(newMethodStep)
            newMeal = Meal(mealData['name'], mealData['description'], ingredients, methodSteps)
            meals.append(newMeal)
        
        return meals
    
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
        numMealsAvailable = len(meals)
        numDays = len(days)

        if numMealsAvailable < numDays:
            mealIndex = 0
            for x in range (numDays):
                days[x].meal = meals[mealIndex]
                mealIndex = mealIndex + 1
                if mealIndex == numMealsAvailable:
                    # run out of meals to plan, so go back to the start of the meal list
                    mealIndex = 0

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
        h=400
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
        mealNameLabel = tk.Label(popupWindowFrame, text=chosenMeal.name)
        mealNameLabel.pack()
        mealDescriptionLabel = tk.Label(popupWindowFrame, text=chosenMeal.description)
        mealDescriptionLabel.pack()
        ingredientsTitleLabel = tk.Label(popupWindowFrame, text="Ingredients:")
        ingredientsTitleLabel.pack()
        for ingredient in chosenMeal.ingredients:
            ingredientLabel = tk.Label(popupWindowFrame, text="• " + ingredient.quantity + " " + ingredient.size + " " + ingredient.units + " " + ingredient.name)
            ingredientLabel.pack()
        methodTitleLabel = tk.Label(popupWindowFrame, text="Method:")
        methodTitleLabel.pack()
        for methodStep in chosenMeal.method:
            methodStepLabel = tk.Label(popupWindowFrame, text=str(methodStep.stepNumber) + ") " + methodStep.stepDescription)
            methodStepLabel.pack()
        no_btn = tk.Button(popupWindowFrame, text="Done", bg="light blue", fg="red", command=closePopupWindow, width=10)
        no_btn.pack()
        popupWindowFrame.grid(column=0, row=0, ipadx=10, ipady=10, sticky="NSEW")

    # Generate 14 days worth of random meals
    def getRandomMeals(self, availableMeals):
        numRandomIndexToGet = 14

        numMealAvailable = len(availableMeals)

        print("numMealAvailable: %d" % (numMealAvailable))

        if numMealAvailable < 14:
            numRandomIndexToGet = numMealAvailable

        randomIndexes = []

        print("numRandomIndexToGet: %d" % (numRandomIndexToGet))

        foundEnoughRandomIndexes = False
        while not foundEnoughRandomIndexes:
            value = randint(0, numMealAvailable-1)
            if value not in randomIndexes:
                randomIndexes.append(value)
            if len(randomIndexes) == numRandomIndexToGet:
                foundEnoughRandomIndexes = True

        chosenMeals = []

        print("randomIndexes len: %d" % (len(randomIndexes)))
        print("randomIndexes[0]: %d" % (randomIndexes[0]))

        for index in randomIndexes:
            chosenMeals.append(availableMeals[index])

        return chosenMeals

    def getDays(self, firstDayOfWeek):
        days = [CalendarDay(firstDayOfWeek, None)]

        dayOfWeek = firstDayOfWeek
        for x in range (13):
            dayOfWeek = dayOfWeek + timedelta(days=1)
            days.append(CalendarDay(dayOfWeek, None))

        return days