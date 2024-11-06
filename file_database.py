from database import Database
import pickle
import os


class FileDatabase(Database):
    def __init__(self, filename='database.pkl'):
        """
        the class inherits from DataBase, gets file name, create lock and save the dict to the file
        :param filename:
        """
        super().__init__()
        self.filename = filename
        # מחיקת המידע הישן שהיה בקובץ
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.dict_to_file()

    def file_to_dict(self):
        """
        load the information from file to dict with pickle
        """
        try:
            with open(self.filename, 'rb') as f:
                self.dict = pickle.load(f)
        except (FileNotFoundError, EOFError):
            print("error in loading file")

    def dict_to_file(self):
        """
        save the dict into the file
        """
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.dict, f)

        except (FileNotFoundError, EOFError):
            print("error in loading the dict to file")

    def set_value(self, key, value):
        """
        load the file to the dict, calls set_value from database with key and value and save the dict with the changes to the file
        :return: the value of set_value
        """
        self.file_to_dict()
        value = super().set_value(key, value)
        self.dict_to_file()
        return value

    def get_value(self, key):
        """
        load the file to the dict, calls get_value from database with key
        :return: the value of original get_value
        """
        self.file_to_dict()
        value = super().get_value(key)
        return value

    def delete_value(self, key):
        """
        load the file to the dict, calls delete_value from database with key  and save the dict with the changes to the file
        :return: the value of original delete_value
        """
        self.file_to_dict()
        value = super().delete_value(key)
        self.dict_to_file()
        return value

