import pickle
import os
import win32file
from database import Database


class FileDatabaseWin(Database):
    def __init__(self, filename='databasewin.pkl'):
        """
        the class inherits from DataBase, gets file name, create lock and save the dict to the file
        :param filename:
        """
        super().__init__()
        self.filename = filename

        self.file = self.create_file()
        self.dict_to_file()


    def create_file(self):
        """
        Creates a file (or opens it) for reading and writing using win32file.
        Ensures the file is not locked by another process.
        :return: File handle
        """
        # אם הקובץ קיים, לא נבצע CREATE_ALWAYS, אלא פתיחה של הקובץ.
        if os.path.exists(self.filename):
            os.remove(self.filename)
        # אם הקובץ לא קיים, ניצור אותו
        handle = win32file.CreateFile(
            self.filename,  # The file name
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,  # Read and write access
            0,  # No sharing
            None,  # Default security attributes
            win32file.CREATE_ALWAYS,  # Create the file if it doesn't exist
            0,  # Additional flags (none)
            None
        )
        handle.close()

        return handle


    def file_to_dict(self):
        """
        Reads the information from the file into a dictionary using pickle.
        """
        try:
            # Open the file for reading
            handle = win32file.CreateFile(
                self.filename,  # File name
                win32file.GENERIC_READ,  # Read-only access
                0,  # No sharing
                None,  # Default security
                win32file.OPEN_EXISTING,  # Open the file if it exists
                0,  # No additional flags
                None
            )
            # Read the data from the file
            hr, data = win32file.ReadFile(handle, os.path.getsize(self.filename))
            # Close the file handle immediately after reading
            handle.close()

            # Unpickle the data into the dictionary
            self.dict = pickle.loads(data)

        except (FileNotFoundError, EOFError) as e:
            print(f"Error in loading file: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def dict_to_file(self):
        """
        Writes the dictionary to the file using pickle.
        """
        try:
            # Serialize the dictionary into bytes
            data = pickle.dumps(self.dict)

            # Open the file for writing
            handle = win32file.CreateFile(
                self.filename,  # The file name
                win32file.GENERIC_WRITE,  # Write-only access
                0,  # No sharing
                None,  # Default security
                win32file.CREATE_ALWAYS,  # Create or overwrite the file
                0,  # No additional flags
                None
            )
            # Write the data to the file
            win32file.WriteFile(handle, data)
            # Close the file handle immediately after writing
            handle.close()
        except Exception as e:
            print(f"Error in writing dict to file: {e}")


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
        load the file to the dict, calls delete_value from database with key and save the dict with the changes to the file
        :return: the value of original delete_value
        """
        self.file_to_dict()
        value = super().delete_value(key)
        self.dict_to_file()
        return value
