#To run this (or any) python file, navigate to folder and type "python <name_of_file>.py"

# This import line tells the computer which python add-ons are needed for it to be able to run the program:
import tkinter as tk
from tkinter import Canvas, BOTH
from datetime import datetime, timedelta
from random import randint

#---------------------------------------------------------------

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # set the title of the main window
        self.title("Meal Planner")

        # set size of the main window to 500 pixels tall and 500 pixels wide
        self.geometry("1000x600")
 
        # Create a container that will contain each page that you can view in the program
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make one grid cell in the container and make it cover the entire window's height
        container.grid_columnconfigure(0,weight=1) # also make that grid cell cover the entire window's width

        # Create an ARRAY that we will use to store all of the pages that we can view in the program
        self.pages = {}

        # In a FOR LOOP, go through each of our available pages and add them to our page array
        for P in (StartPage, Calendar): # for each page
            page = P(container, self) # create the page
            self.pages[P] = page  # store into pages
            page.grid(row=0, column=0, sticky="nsew") # stack the pages in the container's only grid cell
        
        # Call the show page method to show the main menu page when the program first starts.
        self.show_page(StartPage)
 
    # this method/function shows the page that you want to show 
    def show_page(self, name):
        # get the page with this name from our collection of pages and store it in a variable.
        pageToShow = self.pages[name]

        # show the page
        pageToShow.tkraise()
 
#---------------------------------------------------------------

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # create the stuff we want to show on the menu page
        label = tk.Label(self, text='Meal Planner')

        # When this button is clicked, tell the controller to show the 'Meal Planner' page.
        planMealsButton = tk.Button(self, text='Plan some meals!', command=lambda : controller.show_page(Calendar))

        # ley the stuff out where we want it to be ont he menu page
        label.pack(pady=10, padx=10)
        planMealsButton.pack()

#---------------------------------------------------------------

class Calendar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Create the stuff we need to show on this page
        #label = tk.Label(self, text='Player 1 Setup')
        #label.pack(pady=10, padx=10)        

        #TODO: go to player 2 setup
        #backToMainMenuButton = tk.Button(self, text="Done!", command = lambda: controller.show_page(StartPage))

        # Lay the stuff out on the page in the right places

        # Define some colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)

        # This sets the WIDTH and HEIGHT of each grid location
        width = 120
        height = 110

        columnCount = 7
        rowCount = 2

        # This sets the margin between each cell
        margin = 5

        # This sets the padding inside each cell
        padding = 5

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

        randomMeals = getRandomMeals()

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
                topLeftXPosition = (margin + width) * column + margin    
                topLeftYPosition = (margin + height) * row + margin
                bottomRightXPosition = (margin + width) * column + margin + width
                bottomRightYPosition = (margin + height) * row + margin + height
                canvas.create_rectangle(topLeftXPosition, topLeftYPosition, bottomRightXPosition, bottomRightYPosition, outline="red", fill=color)
                textTopLeftXPosition = topLeftXPosition + padding
                textTopLeftYPosition = topLeftYPosition + padding
                textWidth = width - (padding * 2)
                textHeight = height - (padding * 2)
                text = grid[row][column]
                label = tk.Label(self, text=text, wraplength=500, justify="center")
                label.place(x = textTopLeftXPosition, y = textTopLeftYPosition, width=textWidth, height=textHeight)
                
        canvas.pack(fill=BOTH, expand=1)

# Generate 14 days worth of random meals
def getRandomMeals():
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

class Meal:
    def __init__(self, name):
        self.name = name
        #TODO: add ingredients, method, cooking time, serving size, difficulty, equipment, price rating

#---------------------------------------------------------------

# This is the stuff that tells the computer to actually run the program:
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()

#---------------------------------------------------------------