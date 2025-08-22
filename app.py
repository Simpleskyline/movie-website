from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    movie = db.Column(db.String(200), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Home route - form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        movie = request.form["movie"]

        # Save to database
        new_entry = Movie(username=username, movie=movie)
        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for("movies"))
    return render_template("index.html")

# Show all movies
@app.route("/movies")
def movies():
    all_movies = Movie.query.all()
    return render_template("movies.html", movies=all_movies)

if __name__ == "__main__":
    app.run(debug=True)
