from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' hoặc 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    favorites = db.relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Laptop(db.Model):
    __tablename__ = "laptops"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    cpu = db.Column(db.String(120), nullable=False)
    ram_gb = db.Column(db.Integer, nullable=False)
    gpu = db.Column(db.String(120), nullable=True)
    storage = db.Column(db.String(120), nullable=False)
    screen = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)  # VND
    category = db.Column(db.String(80), nullable=False)  # office, student, gaming, design, dev
    image_url = db.Column(db.String(500), nullable=True)
    
    # Thông tin pin
    battery_capacity = db.Column(db.Integer, nullable=True)  # Wh
    battery_life_office = db.Column(db.Integer, nullable=True)  # phút
    battery_life_gaming = db.Column(db.Integer, nullable=True)  # phút
    
    # Điểm số CPU (Geekbench 6)
    cpu_single_core_plugged = db.Column(db.Integer, nullable=True)
    cpu_multi_core_plugged = db.Column(db.Integer, nullable=True)
    cpu_single_core_battery = db.Column(db.Integer, nullable=True)
    cpu_multi_core_battery = db.Column(db.Integer, nullable=True)
    
    # Điểm số GPU (3DMark hoặc Geekbench)
    gpu_score_plugged = db.Column(db.Integer, nullable=True)
    gpu_score_battery = db.Column(db.Integer, nullable=True)

    favorites = db.relationship("Favorite", back_populates="laptop", cascade="all, delete-orphan")

class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    laptop_id = db.Column(db.Integer, db.ForeignKey("laptops.id"), nullable=False)

    user = db.relationship("User", back_populates="favorites")
    laptop = db.relationship("Laptop", back_populates="favorites")
