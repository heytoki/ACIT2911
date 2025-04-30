from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from db import db

app = Flask(__name__)

# placeholder -> will get recipes from our database
recipes = []

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
app.instance_path = Path("data").resolve()

db.init_app(app)
@app.route('/')
def home():
    return render_template('home.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True, port=5555)
