#!/usr/bin/python3
"""module that defines a class to handle db storage for hbnb"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

classes = {
    'State': State,
    'City': City,
    'User': User,
    'Review': Review,
    'Amenity': Amenity,
    'Place': Place
}


class DBStorage:
    """class definition for db storage"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializing DBStorage instance"""
        user = os.environ.get("HBNB_MYSQL_USER")
        pwd = os.environ.get("HBNB_MYSQL_PWD")
        host = os.environ.get("HBNB_MYSQL_HOST")
        db = os.environ.get("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
            )

        if os.environ.get("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        obj_dict = {}

        if cls in classes.keys():
            for row in self.__session.query(cls).all():
                cls_name = classes[cls].__name__
                key = f"{cls_name}.{row.id}"
                obj_dict[key] = row
        else:
            table_rows = []
            for key, value in classes.items():
                table_rows.append(self.__session.query(value).all())
            for rows in table_rows:
                for row in rows:
                    cls_name = type(row).__name__
                    key = f"{cls_name}.{row.id}"
                    obj_dict[key] = row

        return obj_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and create the current database session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        sessions = scoped_session(Session)
        self.__session = sessions()

    def close(self):
       """Closes a session"""
       self.__session.close()
