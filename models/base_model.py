#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
# from models import storage


Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        str_rep = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            if 'id' not in kwargs.keys():
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs.keys():
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs.keys():
                self.updated_at = datetime.now()

            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, str_rep)
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()


    def __str__(self):
        """Returns a string representation of the instance"""
        return f"[{type(self).__name__}] ({self.id}) {self.to_dict()}"
        # cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        # return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary['__class__'] = type(self).__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        del dictionary["_sa_instance_state"]
        # dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        # from models import storage
        storage.delete(self)
