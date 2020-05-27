class Meal:
    def __init__(self, name, description, ingredients, method, difficultyRating, equipment, priceRating, dietaryNotes, prepTime, cookingTime):
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.method = method
        self.difficultyRating = difficultyRating
        self.equipment = equipment
        self.priceRating = priceRating
        self.dietaryNotes = dietaryNotes
        self.prepTime = prepTime
        self.cookingTime = cookingTime
        self.totalTime = self.prepTime + self.cookingTime
        #TODO: add active vs passive cooking time, serving size