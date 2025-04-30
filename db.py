from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Recipes(DeclarativeBase):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Ingredients(DeclarativeBase):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parameter = Column(String, nullable=False)

db = SQLAlchemy(model_class=Recipes)