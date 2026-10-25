from flask import Flask, jsonify, request
from flask_migrate import Migrate
from server.models import db, Book

app = Flask(__name__)

#Database migrations
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookworm.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return jsonify({
        "message":"Welcome to BookWorm Central API"
    })
    
@app.route("/books", methods=["GET"])
def get_books():
    books = db.session.execute(
        db.select(Book).order_by(Book.id)
    ).scalars().all()
    
    return jsonify([book.to_dict() for book in books])

@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json(silent=True)
    
    if not isinstance(data, dict):
        return jsonify({"error": "Title is required"}), 400
    
    title = data.get("title")
    author = data.get("author")
    
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error":"Title is required"}), 400
    
    if not isinstance(author, str) or not author.strip():
            return jsonify({"error":"Author is required"}), 400
    
    book = Book(
        title=title.strip(),
        author=author.strip()
    )
    
    db.session.add(book)
    db.session.commit()
    
    return jsonify(book.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)