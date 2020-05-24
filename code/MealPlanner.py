#To run this (or any) python file, navigate to folder and type "python <name_of_file>.py"

# This import line tells the computer which python add-ons are needed for it to be able to run the program:
import tkinter as tk
from MainMenuPage import MainMenuPage
from CalendarPage import CalendarPage

#---------------------------------------------------------------

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # set the title shown in the title bar of the main window
        self.title("Meal Planner")

        # set size of the main window
        windowWidth = 880
        windowHeight = 400
        self.geometry(str(windowWidth) + "x" + str(windowHeight))
 
        # Create a container that will contain each page that you can view in the program
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make one grid cell in the container and make it cover the entire window's height
        container.grid_columnconfigure(0,weight=1) # also make that grid cell cover the entire window's width

        # Create an ARRAY that we will use to store all of the pages that we can view in the program
        self.pages = {}

        # In a FOR LOOP, go through each of our available pages and add them to our page array
        for P in (MainMenuPage, CalendarPage): # for each page
            page = P(container, self) # create the page
            self.pages[P] = page  # store into pages
            page.grid(row=0, column=0, sticky="nsew") # stack the pages in the container's only grid cell
        
        # Call the show page method to show the main menu page when the program first starts.
        self.show_page(MainMenuPage)
 
    # this method/function shows the page that you want to show 
    def show_page(self, name):
        # get the page with this name from our collection of pages and store it in a variable.
        pageToShow = self.pages[name]

        # show the page
        pageToShow.tkraise()

#---------------------------------------------------------------

# This is the stuff that tells the computer to actually run the program:
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()

#---------------------------------------------------------------