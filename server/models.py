from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    # Validators
    @validates("name")
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Author must have a name.")
        
        # Check for duplicates in the database
        existing = Author.query.filter(Author.name == name.strip()).first()
        if existing and existing.id != self.id:
            raise ValueError("Author name must be unique.")
        
        return name.strip()

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if not phone_number or len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Author phone number must be exactly 10 digits.")
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    # Validators
    @validates("title")
    def validate_title(self, key, title):
        if not title or title.strip() == "":
            raise ValueError("Post title cannot be empty.")
        
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait_words):
            raise ValueError(
                f"Post title must be clickbait-y and contain one of: {', '.join(clickbait_words)}"
            )
        return title.strip()

    @validates("content")
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary cannot exceed 250 characters.")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        allowed = ["Fiction", "Non-Fiction"]
        if category not in allowed:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
