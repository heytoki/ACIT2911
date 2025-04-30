# models.py
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, Text

class Base(DeclarativeBase):
    pass

class Recipe(Base):
    __tablename__ = "recipes"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String, nullable=False)
    ingredients = mapped_column(Text, nullable=False)
    instructions = mapped_column(Text)
    category = mapped_column(String)

    def __repr__(self):
        return f"<Recipe {self.title}>"
