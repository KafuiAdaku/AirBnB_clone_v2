#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
import os

storage_type = os.getenv('HBNB_TYPE_STORAGE')
class Amenity(BaseModel, Base):
    __tablename__ = "amenities"
    if storage_type == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity",
                back_populates="amenities")
    else:
        name = ""
