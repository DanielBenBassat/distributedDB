from database import Database
import pickle
from multiprocessing import Lock
import os

class FileDatabase(Database):
    def __init__(self, filename='database.pkl'):
        """
        the class inherits from DataBase, gets file name, create lock and save the dict to the file
        :param filename:
        """
        super().__init__()
        self.filename = filename
        if os.path.exists(self.filename):
            os.remove(self.filename)  # מחיקה של הקובץ הישן
        with open(self.filename, 'wb') as f:
            pickle.dump(self.dict, f)  # יצירת קובץ חדש ושמיר
    def load(self):
        """
        load the information from file to dict with pickle
        """
        try:
            with open(self.filename, 'rb') as f:
                self.dict = pickle.load(f)
        except (FileNotFoundError, EOFError):
            print("error in loading file")

    def save(self):
        """
        save the dict into the file
        """
        try:
            #שמירת המידע שקיים בקובץ
            with open(self.filename, 'rb') as f:
                data = pickle.load(f)


        #העלאת המידע המידע של הקובץ והמילון לקובץ
            with open(self.filename, 'wb') as f:
                pickle.dump(self.dict, f)
                pickle.dump(data, f)

        except (FileNotFoundError, EOFError):
            print("error in loading the dict to file")

    def set_value(self, key, value):
        """
        load the file to the dict, calls set_value from database with key and value and save the dict with the changes to the file
        :return: the value of set_value
        """
        #self.load()
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

