#!/usr/bin/python3
import json
import os
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
        Sets in __objects the obj with key <obj class name>.id.
        Args:
            obj: The object to be stored.
        Returns:
            None
        """
        obj_cls_name = obj.__class__.__name__
        key = "{}.{}".format(obj_cls_name, obj.id)
        FileStorage.__objects[key] = obj

    def all(self):
        """
        Returns the dictionary __objects.
        Returns:
            dict: The dictionary containing stored objects.
        """
        return FileStorage.__objects

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        Returns:
            None
        """
        all_objs = FileStorage.__objects
        obj_dict = {}
        for obj in all_objs.keys():
            obj_dict[obj] = all_objs[obj].to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists;
        otherwise, do nothing. If the file doesn’t exist,
        no exception should be raised).
        Returns:
            None
        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                try:
                    obj_dict = json.load(file)
                    for key, values in obj_dict.items():
                        class_name, obj_id = key.split('.')
                        cls = eval(class_name)
                        instance = cls(**values)
                        FileStorage.__objects[key] = instance
                except Exception:
                    pass
