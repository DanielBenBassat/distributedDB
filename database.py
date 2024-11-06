
class Database:
    def __init__(self):
        """
        create a new empty dict and general lock for all function in Database
        """
        self.dict = {}

    def set_value(self, key, value):
        """
        set new value and key in dictionary
        :return: true if succeed and false if not
        """
        success = False
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
        try:
            if key in self.dict:
                value = self.dict[key]
            else:
                print("not in")
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
        try:
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


def run_tests(self):
    """
    Run a series of tests to check of the Database class.
    """
    assert self.set_value("name", "daniel") is True
    assert self.set_value("age", "17") is True

    assert self.get_value("name") == "daniel"
    assert self.get_value("age") == 17

    assert self.get_value("school") is None

    assert self.delete_value("name") == "daniel"
    assert self.get_value("name") is None, "key1 should no longer exist after deletion"
    assert self.delete_value("age") == "17"

    assert self.dict == {}





