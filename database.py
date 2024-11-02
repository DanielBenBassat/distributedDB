from threading import Lock


class Database:
    def __init__(self):
        """
        create a new empty dict and general lock for all function in Database
        """
        self.dict = {}
        self.lock = Lock()

    def set_value(self, key, value):
        """
        set new value and key in dictionary
        :return: true if succeed and false if not
        """
        success = False
        with self.lock:
            try:
                self.dict[key] = value
                success = True
            except Exception as e:
                print(f"Error while setting value: {e}")
                success = False
            finally:
                return success

    def get_value(self, key):
        """
        read the value of the given key and return it
        :param key: key in dict
        :return: value of the key, none if not exists
        """
        value = None
        with self.lock:
            try:
                if key in self.dict:
                    value = self.dict[key]
                else:
                    value = None
            except Exception as e:
                print(f"Error while getting value: {e}")
                value = None
            finally:
                return value

    def delete_value(self, key):
        """
        deletes the value of the key and returns it
        :param key: key in dict
        :return: the value that has deleted
        """
        value = None
        with self.lock:
            try:
                with self.lock:
                    if key in self.dict:
                        value = self.dict[key]
                        del self.dict[key]
                    else:
                        value = None
            except Exception as e:
                print(f"Error while deleting value: {e}")
                value = None
            finally:
                return value



    def print_dict(self):
        if self.dict:
            print("Current Dictionary:")
            for key, value in self.dict.items():
                print(f"{key}: {value}")
        else:
            print("The dictionary is empty.")








