#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os

storage_type = os.environ.get("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """State class"""

    __tablename__ = "states"

    if storage_type == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """Getter attribute that return associated cities"""
            from models.city import City
            from models import storage

            return [
                city for city in storage.all(City).values()
                if city.state_id == self.id]

        @property
        def cities(self):
            """Returns a list of `City` objects from `storage` linked to the
                current `State`"""
            from models import storage
            city_list = storage.all("City").values()
            return [obj for obj in city_list if obj.state_id == self.state.id]
