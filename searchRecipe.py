from models import Recipe, Ingredient
from sqlalchemy import and_
def searchFunc(query, filterType, param):
    if filterType == 'title':
        return Recipe.query.filter(Recipe.title.like('%'+query+'%')).all()
    if filterType == 'cuisine':
        if param == 'italian':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.cuisine.like('italian')
            )).all()
        if param == 'chinese':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.cuisine.like('chinese')
            )).all()
        if param == 'thai':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.cuisine.like('thai')
            )).all()
        if param == 'indian':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.cuisine.like('indian')
            )).all()
        if param == 'french':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.cuisine.like('french')
            )).all()
        if param == 'japanese':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.cuisine.like('japanese')
            )).all()
        if param == 'mexican':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.cuisine.like('mexican')
            )).all()
        if param == 'other':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.cuisine.like('other')
            )).all()        
        
    if filterType == 'time':
        return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.cook_time <= param
        )).all()

    if filterType == 'diff':
        if param == 'hard':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.difficulty.like('hard')
            )).all()
        if param == 'medium':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.difficulty.like('medium')
            )).all()
        if param == 'easy':
            return Recipe.query.filter(and_(
                Recipe.title.like('%'+query+'%'),
                Recipe.difficulty.like('easy')
            )).all()