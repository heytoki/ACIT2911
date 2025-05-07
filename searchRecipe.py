from models import Recipe, Ingredient

def searchFunc(query, filterType):
    if filterType == 'title':
        return Recipe.query.filter(Recipe.title.like('%'+query+'%')).all()
    if filterType == 'cuisine':
        return Recipe.query.filter(Recipe.cuisine.like('%'+query+'%')).all()
    if filterType == 'time':
        return Recipe.query.filter(Recipe.cook_time.like('%'+query+'%')).all()
    if filterType == 'diff':
        return Recipe.query.filter(Recipe.difficulty.like('%'+query+'%')).all()