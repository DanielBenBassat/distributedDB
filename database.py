import pickle
import threading
from threading import Lock

class Database:
    def __init__(self, filename='database.pkl'):
        self.dict = {}
        self.filename = filename
        self.lock = Lock()
        self.load()

    def load(self):
        """
        load the information from file to mdict with pickle
        """
        try:
            with open(self.filename, 'rb') as f:
                self.dict = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.dict = {}

    def save(self):
        """
        save the dict into the file
        """
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.dict, f)
        except (FileNotFoundError, EOFError):
            pass

    def set_value(self, key, value):
        try:
            with self.lock:
                self.dict[key] = value
                self.save()
                return True
        except Exception as e:
            print(f"Error while setting value: {e}")
            return False

    def get_value(self, key):
        try:
            with self.lock:
                if key in self.dict:
                    value = self.dict[key]
                else:
                    value = None
                return value
        except Exception as e:
            print(f"Error while getting value: {e}")
            return None

    def delete_value(self, key):
        try:
            with self.lock:
                if key in self.dict:
                    value = self.dict[key]
                    del self.dict[key]
                    self.save()
                    return value
                else:
                    return None
        except Exception as e:
            print(f"Error while deleting value: {e}")
            return None


    def print_dict(self):
        if self.dict:
            print("Current Dictionary:")
            for key, value in self.dict.items():
                print(f"{key}: {value}")
        else:
            print("The dictionary is empty.")








