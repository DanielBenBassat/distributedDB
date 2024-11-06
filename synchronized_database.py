from file_database import FileDatabase
import threading
import multiprocessing
import os
import logging
import time

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/synchronized.log'


class SynchronizedDatabase(FileDatabase):
    def __init__(self, filename, mode, max_readers=10):
        """
        initialize synchronized database that inherits from FileDatabase, create locks and semaphore according to mode
        available_semaphore_taking: true if you have access for taking semaphore and false if not. avoid competition on taking semaphore,
        the first writer or reader to arrive will be the first to get a semaphore
        :param filename: file name
        :param mode: threads or multiprocessing
        :param max_readers:
        """
        super().__init__(filename)
        self.mode = mode
        self.max_readers = max_readers
        self.available_semaphore_taking = True
        if self.mode == "threads":
            self.semaphore = threading.Semaphore(max_readers)
            self.write_lock = threading.Lock()
            self.read_lock = threading.Lock()
        else:
            self.semaphore = multiprocessing.Semaphore(max_readers)
            self.write_lock = multiprocessing.Lock()
            self.read_lock = multiprocessing.Lock()

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
        self.semaphore.acquire()
        self.read_lock.acquire()

    def release_read_lock(self):
        """
        Releases the read lock, decrementing the semaphore to allow other readers or writers.
        """
        self.semaphore.release()
        self.read_lock.release()


    def acquire_write_lock(self):
        """
        takes lock_for_semaphore_acquire to be the first one to take semaphoe when its realised, and then take all the semaphores until have all of them and takes the write_lock
        """
        while True:
            while self.available_semaphore_taking:
                logging.debug("writer is waiting")
                self.available_semaphore_taking = False
                count = 0
                while count < self.max_readers:
                    self.semaphore.acquire()
                    count += 1
                    logging.debug(count)
                self.write_lock.acquire()
                return

    def release_write_lock(self):
        """
        realise the semaphores and the write lock
        :return:
        """
        for i in range(self.max_readers):
            self.semaphore.release()
        self.write_lock.release()
        self.available_semaphore_taking = True

    def set_value(self, key, value):
        self.acquire_write_lock()
        result = False
        try:
            result = super().set_value(key, value)
        finally:
            self.release_write_lock()
            logging.debug("Write completed.")
            return result

    def get_value(self, key):
        self.acquire_read_lock()
        value = None
        try:
            value = super().get_value(key)
        finally:
            logging.debug(f"Read value: {value}")
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







