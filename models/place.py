#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
import os


storage_type = os.getenv('HBNB_TYPE_STORAGE')
place_amenity = Table("place_amenity", Base.metadata,
        Column("place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
            nullable=False),
        Column("amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True,
            nullable=False)
        )

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if storage_type == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0,  nullable=False)
        number_bathrooms = Column(Integer, default=0,  nullable=False)
        max_guest = Column(Integer, default=0,  nullable=False)
        price_by_night = Column(Integer, default=0,  nullable=False)
        latitude = Column(Float, default=0,  nullable=True)
        longitude = Column(Float, default=0,  nullable=True)
        reviews = relationship("Review", backref="place",
                cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary="place_amenity",
                viewonly=False, back_populates="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """returns the list of `Review` instances with `place_id`
            equals to the current `Place.id`"""
            from models import storage
            rev_list = []
            reviews = storage.all(Review)
            places = storage.all(Places)
            for pk,pv in places.items():
                for rk,rv in reviews.items():
                    if pv.id == rv.id:
                        rev_list.append(rv)
            return rev_list

        if os.getenv('HBNB_TYPE_STORAGE') != "db":
            @property
            def amenities(self):
                """returns the list of `Amenity` instances based on the attribute
                `amenity_ids` that contains all `Amenity.id` linked to the `Place`
                """
                from models import storage
                amenity_obj = []
                all_amenities = storage.all(Amentiy)
                for amenity_id in amenity_ids:
                    for k,v in all_amenities.items():
                        if amenity_id in k:
                            amenity_obj.append(v)
                return amenity_obj

            @amenities.setter
            def amenities(self, amenity):
                """setter"""
                if isinstance(amenity, Amenity):
                    self.amenity_ids.append(amenity.id)
