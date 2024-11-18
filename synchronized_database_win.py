from file_database import FileDatabase
from pywin32_file import FileDatabaseWin
import win32file
import win32event
import os
import logging
import time


LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/synchronized.log'


class SynchronizedDatabase(FileDatabaseWin):
    def __init__(self, filename,mode, max_readers=10):
        """
        initialize synchronized database that inherits from FileDatabase, create locks and semaphore according to mode
        available_semaphore_taking: true if you have access for taking semaphore and false if not. avoid competition on taking semaphore,
        the first writer or reader to arrive will be the first to get a semaphore
        :param filename: file name
        :param mode: threads or multiprocessing
        :param max_readers:
        """
        super().__init__(filename)
        self.available_semaphore_taking = True
        self.max_readers = max_readers
        self.reader_semaphore = win32event.CreateSemaphore(None, max_readers, max_readers, None)
        self.write_mutex = win32event.CreateMutex(None, False, None)
        self.read_mutex = win32event.CreateMutex(None, False, None)

        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
            logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    def acquire_read_lock(self):
        """
        Acquires the read lock, allowing multiple readers to read together.
        It blocks if the max number of readers is above 10
        """

        while not self.available_semaphore_taking:
            pass
        win32event.WaitForSingleObject(self.reader_semaphore, win32event.INFINITE)
        win32event.WaitForSingleObject(self.read_mutex, win32event.INFINITE)

    def release_read_lock(self):
        """
        Releases the read lock, decrementing the semaphore to allow other readers or writers.
        """
        win32event.ReleaseSemaphore(self.reader_semaphore, 1)
        win32event.ReleaseMutex(self.read_mutex)


    def acquire_write_lock(self):
        """
        takes lock_for_semaphore_acquire to be the first one to take semaphoe when its realised, and then take all the semaphores until have all of them and takes the write_lock
        """
        while True:
            while self.available_semaphore_taking:
                print("writer is waiting")
                self.available_semaphore_taking = False
                count = 0
                while count < self.max_readers:
                    win32event.WaitForSingleObject(self.reader_semaphore, win32event.INFINITE)
                    count += 1
                    print(count)
                win32event.WaitForSingleObject(self.write_mutex, win32event.INFINITE)
                return

    def release_write_lock(self):
        """
        realise the semaphores and the write lock
        :return:
        """
        for i in range(self.max_readers):
            win32event.ReleaseSemaphore(self.reader_semaphore, 1)
        win32event.ReleaseMutex(self.write_mutex)
        self.available_semaphore_taking = True

    def set_value(self, key, value):
        self.acquire_write_lock()
        result = False
        try:
            result = super().set_value(key, value)
        finally:
            self.release_write_lock()
            print("Write completed.")
            return result

    def get_value(self, key):
        self.acquire_read_lock()
        value = None
        try:
            value = super().get_value(key)
        finally:
            print(f"Read value: {value}")
            self.release_read_lock()
            return value

    def delete_value(self, key):
        self.acquire_write_lock()
        result = False
        try:
            result = super().delete_value(key)
        finally:
            self.release_write_lock()
            return result







