import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))

    favorite_planets = relationship("FavoritePlanet", back_populates="user")
    favorite_characters = relationship("FavoriteCharacter", back_populates="user")
    blog_posts = relationship("BlogPost", back_populates="author")

class Planet(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    climate = Column(String(250))
    terrain = Column(String(250))
    population = Column(Integer)
    diameter = Column(Integer)
    gravity = Column(String(50))

    favorited_by = relationship("FavoritePlanet", back_populates="planet")
    characters = relationship("Character", back_populates="home_planet")

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    height = Column(Integer)
    mass = Column(Integer)
    hair_color = Column(String(50))
    eye_color = Column(String(50))
    birth_year = Column(String(10))
    gender = Column(Enum('Male', 'Female', 'Other', name='gender_types'))
    home_planet_id = Column(Integer, ForeignKey('planets.id'))

    home_planet = relationship("Planet", back_populates="characters")
    favorited_by = relationship("FavoriteCharacter", back_populates="character")

class FavoritePlanet(Base):
    __tablename__ = 'favorite_planets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    planet_id = Column(Integer, ForeignKey('planets.id'))

    user = relationship("User", back_populates="favorite_planets")
    planet = relationship("Planet", back_populates="favorited_by")

class FavoriteCharacter(Base):
    __tablename__ = 'favorite_characters'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    character_id = Column(Integer, ForeignKey('characters.id'))

    user = relationship("User", back_populates="favorite_characters")
    character = relationship("Character", back_populates="favorited_by")

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    content = Column(String(5000), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    
    author = relationship("User", back_populates="blog_posts")

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')