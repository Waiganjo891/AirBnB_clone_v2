#!/usr/bin/pythoni3
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

Base = declarative_base()


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

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        __init__ - Initializes a new instance of the BaseModel.

        Usage:
            my_model = BaseModel()
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(
                            value, "%Y-<S-F10>%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def save(self):
        """
        save - Updates the 'updated_at' attribute to the current timestamp.
        Usage:
            my_model.save()
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        to_dict - Converts the model instance to a dictionary.
        Returns:
            dict: A dictionary containing the model's attributes.
        Usage:
            my_model_dict = my_model.to_dict()
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop("_sa_instance_state", None)
        return my_dict

    def delete(self):
        """
        Delete the current instance from storage
        """
        models.storage.delete(self)

    def __str__(self):
        """
        __str__ - Returns a string representation of the model.
        Returns:
            str: A string representation of the model.
        Usage:
            print(my_model)
        """
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)


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
