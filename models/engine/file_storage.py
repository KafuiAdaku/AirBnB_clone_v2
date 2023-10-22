#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        # if cls is None:
        #     return FileStorage.__objects
        # else:
        #     filtered_objects = {}
        #     for key, obj in FileStorage.__objects.items():
        #         if type(obj) == cls:
        #             filtered_objects = obj
        #     return filtered_objects
        classes = ["BaseModel", "User", "State", "City",
                   "Amenity", "Place", "Review"]
        if cls:
            filtered_objects = {}

            if cls.__name__ in classes:
                for key, obj in FileStorage.__objects.items():
                    if key.split('.')[0] == cls.__name__:
                        filtered_objects[key] = obj
            return filtered_objects
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        # self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        # with open(FileStorage.__file_path, 'w') as f:
        #     temp = {}
        #     temp.update(FileStorage.__objects)
        #     for key, val in temp.items():
        #         temp[key] = val.to_dict()
        #     json.dump(temp, f)
        data = {}
        for key, value in FileStorage.__objects.items():
            data[key] = value.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(data, file)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        # classes = {
        #             'BaseModel': BaseModel, 'User': User, 'Place': Place,
        #             'State': State, 'City': City, 'Amenity': Amenity,
        #             'Review': Review
        #           }
        # try:
        #     temp = {}
        #     with open(FileStorage.__file_path, 'r') as f:
        #         temp = json.load(f)
        #         for key, val in temp.items():
        #                 self.all()[key] = classes[val['__class__']](**val)
        try:
            with open(FileStorage.__file_path, "r") as f:
                dict_ob = json.load(f)
                for key, value in dict_ob.items():
                    class_name = value["__class__"]
                    obj = eval(class_name)(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from __objects if it exists"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            # if key in FileStorage.__objects:
            #     del FileStorage.__objects[key]
            #     self.save()
            del FileStorage.__objects[key]

    def close(self):
        """Deslerializes the JSON file to objcts"""
        self.reload()
