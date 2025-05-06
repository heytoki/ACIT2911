from models import Recipe, Ingredient

def searchFunc(query):
    return Recipe.query.filter(Recipe.title.like('%'+query+'%')).all()