#!/usr/bin/python3
import uuid
from datetime import datetime
import models


class BaseModel:
    """
    BaseModel - A base class for models.

    Attributes:
        id (str): A unique identifier generated using the uuid module.
        created_at (datetime): The timestamp representing the
        creation time of the model.
        updated_at (datetime): The timestamp representing the
        last update time of the model.

    Methods:
        __init__(): Initializes a new instance of the BaseModel.
        save(): Updates the 'updated_at' attribute to the current timestamp.
        to_dict(): Converts the model instance to a dictionary.
        __str__(): Returns a string representation of the model.

    Usage:
        my_model = BaseModel()
        my_model.save()
        my_model_dict = my_model.to_dict()
        print(my_model)
    """
    def __init__(self, *args, **kwargs):
        """
        __init__ - Initializes a new instance of the BaseModel.

        Usage:
            my_model = BaseModel()
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value, time_format))
                else:
                    setattr(self, key, value)

        models.storage.new(self)

    def save(self):
        """
        save - Updates the 'updated_at' attribute to the current timestamp.
        Usage:
            my_model.save()
        """
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """
        to_dict - Converts the model instance to a dictionary.
        Returns:
            dict: A dictionary containing the model's attributes.
        Usage:
            my_model_dict = my_model.to_dict()
        """
        inst_dict = self.__dict__.copy()
        inst_dict["__class__"] = self.__class__.__name__
        inst_dict["created_at"] = self.created_at.isoformat()
        inst_dict["updated_at"] = self.updated_at.isoformat()

        return inst_dict

    def __str__(self):
        """
        __str__ - Returns a string representation of the model.
        Returns:
            str: A string representation of the model.
        Usage:
            print(my_model)
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)


if __name__ == "__main__":
    my_model = BaseModel()
    my_model.name = "My First Model"
    my_model.my_number = 89
    print(my_model)
    my_model.save()
    print(my_model)
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(
            key, type(my_model_json[key]), my_model_json[key]
        ))
