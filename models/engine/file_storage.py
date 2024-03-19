#!/usr/bin/python3
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    This class represents a file-based storage system for managing objects
    in a JSON file.
    Attributes:
        __file_path (str): The path to the JSON file.
        __objects (dict): A dictionary to store objects by <class name>.id.
    Methods:
        new(self, obj):
            Sets in __objects the obj with key <obj class name>.id.
        all(self):
            Returns the dictionary __objects.
        save(self):
            Serializes __objects to the JSON file (path: __file_path).
        reload(self):
            Deserializes the JSON file to __objects (only if the JSON file
            (__file_path) exists;
            otherwise, do nothing. If the file doesn’t exist, no exception
            should be raised).
    """
    __file_path = "file.json"
    __objects = {}

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def all(self, cls=None):
        """
        Returns the dictionary __objects.
        Returns:
            dict: The dictionary containing stored objects.
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for k, v in self.__objects.items():
                if type(v) == cls:
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        odict = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(odict, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists;
        otherwise, do nothing. If the file doesn’t exist,
        no exception should be raised).
        Returns:
            None
        """
        try:
            with open(self.__file_path, "r",  encoding="utf-8") as f:
                for o in json.load(f).values():
                    name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(name)(**o))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Delete a given object from __objects, if it exists
        """
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """
        Call the reload method
        """
        self.reload()
