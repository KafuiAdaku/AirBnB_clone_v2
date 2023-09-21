#!/usr/bin/python3
"""Database storage for objects"""
from models.base_model import Base
# from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os



class DBStorage:
    """Storage class"""
    __engine = None
    __session = None
    classes = {
        'State': State,
        'City': City,
        'User': User,
        'Review': Review,
        'Amenity': Amenity,
        'Place': Place
    }

    def __init__(self):
        """initialises the engine"""
        username = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv("HBNB_ENV")
        self.__engine = create_engine(f"mysql+mysqldb://"
                f"{username}:{password}"
                f"@{host}:"
                f"3306/{database}"
                , pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (`self.__session`)
        all objects depending on the class name (argument `cls`)
        """
        # from models import storage
        obj_dict = {}
        if cls is not None and cls in self.classes:
            all_obj = self.__session.query(self.classes[cls]).all
            for obj in all_obj:
                cls_name = type(obj).__name__
                key = f"{cls_name}.{obj.id}"
                obj_dict[key] = obj
            return obj_dict
        if cls is None:
            all_obj = []
            for k,v in self.classes.items():
                all_obj.extend( self.__session.query(v).all())
            for obj in all_obj:
                cls_name = type(obj).__name__
                key = f"{cls_name}.{obj.id}"
                obj_dict[key] = obj
            return obj_dict

    def new(self, obj):
        """adds the object to the current database session (`self.__session`)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session (`self.__session`)"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session `obj` if not `None`"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
