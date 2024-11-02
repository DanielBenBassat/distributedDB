from database import Database
import pickle
from threading import Lock


class FileDatabase(Database):
    def __init__(self, filename='database.pkl'):
        """
        the class inherits from DataBase, gets file name, create lock and save the dict to the file
        :param filename:
        """
        super().__init__()
        self.filename = filename
        self.lock = Lock()
        self.save()

    def load(self):
        """
        load the information from file to dict with pickle
        """
        try:
            with self.lock:
                with open(self.filename, 'rb') as f:
                    self.dict = pickle.load(f)
        except (FileNotFoundError, EOFError):
            print("error in loading file")

    def save(self):
        """
        save the dict into the file
        """
        try:
            with self.lock:
                with open(self.filename, 'wb') as f:
                    pickle.dump(self.dict, f)
        except (FileNotFoundError, EOFError):
            pass

    def set_value(self, key, value):
        """
        load the file to the dict, calls set_value from database with key and value and save the dict with the changes to the file
        :return: the value of set_value
        """
        self.load()
        value = super().set_value(key, value)
        self.save()
        return value



    def get_value(self, key):
        """
        load the file to the dict, calls get_value from database with key
        :return: the value of original get_value
        """
        self.load()
        value = super().get_value(key)
        return value


    def delete_value(self, key):
        """
        load the file to the dict, calls delete_value from database with key  and save the dict with the changes to the file
        :return: the value of original delete_value
        """
        self.load()
        value = super().delete_value(key)
        self.save()
        return value

