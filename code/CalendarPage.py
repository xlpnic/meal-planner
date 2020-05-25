import tkinter as tk
from tkinter import Canvas, BOTH, Frame
from datetime import datetime, timedelta
from random import randint
from Meal import Meal

class CalendarPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 

        #TODO: navigate back to menu page
        #backToMainMenuButton = tk.Button(self, text="Back to menu", command = lambda: controller.show_page(MainMenuPage))

        # This sets the WIDTH and HEIGHT of each grid location
        cellWidth = 120
        cellHeight = 110

        #This sets the margin between each cell
        cellMargin = 5

        # This sets the padding inside each cell
        cellPadding = 5

        columnCount = 7
        rowCount = 2
        
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

        print("firstDayOfWeek: " + str(firstDayOfWeek))

        dayOfWeek = firstDayOfWeek

        randomMeals = self.getRandomMeals()

        # Create a 2 dimensional array. A two dimensional array is simply a list of lists.
        grid = []
        for row in range(rowCount):
            # Add an empty array that will hold each cell in this row
            grid.append([])
            for column in range(columnCount):
                grid[row].append(0)  # Append a cell
                mealIndex = (row * 7) + column
                meal = randomMeals[mealIndex]
                grid[row][column] = dayOfWeek.strftime("%a %d %b") + "\n\n" + meal.name
                dayOfWeek = dayOfWeek + timedelta(days=1)

        # Loop until the user clicks the close button.
        done = False
        
        canvas = Canvas(self)
        
        # Draw the grid
        for row in range(rowCount):
            for column in range(columnCount):
                color = "white"
                if grid[row][column] == datetime.today().strftime("%a %d %b"):
                    # Highlight the current day as green, if it is present in the view.
                    color = "green"
                topLeftXPosition = (cellMargin + cellWidth) * column + cellMargin    
                topLeftYPosition = (cellMargin + cellHeight) * row + cellMargin
                bottomRightXPosition = (cellMargin + cellWidth) * column + cellMargin + cellWidth
                bottomRightYPosition = (cellMargin + cellHeight) * row + cellMargin + cellHeight
                canvas.create_rectangle(topLeftXPosition, topLeftYPosition, bottomRightXPosition, bottomRightYPosition, outline="red", fill=color)
                textTopLeftXPosition = topLeftXPosition + cellPadding
                textTopLeftYPosition = topLeftYPosition + cellPadding
                textWidth = cellWidth - (cellPadding * 2)
                textHeight = cellHeight - (cellPadding * 2)
                cellText = grid[row][column]
                #label = tk.Label(self, text=text, wraplength=500, justify="center")
                #label.place(x = textTopLeftXPosition, y = textTopLeftYPosition, width=textWidth, height=textHeight)
                #TODO: right now, this always passes through the last cell's data. Need to change it so that each button has unique data.
                showMealButton = tk.Button(self, text=cellText, command=lambda : self.popup_meal(cellText))
                showMealButton.place(x = textTopLeftXPosition, y = textTopLeftYPosition, width=textWidth, height=textHeight)
                
        canvas.pack(fill=BOTH, expand=1)

    def popup_meal(self, val):
        #TODO: set a modal overlay on main window whilst this window is open.
        qw=tk.Tk()
        frame1 = Frame(qw, highlightbackground="green", highlightcolor="green",highlightthickness=1, bd=0)
        frame1.pack()
        qw.overrideredirect(1)
        #TODO: get this to appear in the centre of the main window...
        qw.geometry("200x200+100+100")
        lbl = tk.Label(frame1, text="Meal_" + str(val))
        lbl.pack()
        no_btn = tk.Button(frame1, text="Done", bg="light blue", fg="red",command=qw.destroy, width=10)
        no_btn.pack(padx=10, pady=10)
        qw.mainloop()

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