from file_database import FileDatabase
import threading
import multiprocessing
import os
import logging

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/synchronized.log'


class SynchronizedDatabase(FileDatabase):
    def __init__(self, filename, mode, max_readers=10):
        """
        initialize synchronized database that inherits from FileDatabase, create locks and semaphore according to mode
        :param filename: file name
        :param mode: threads or multiprocessing
        :param max_readers:
        """
        super().__init__(filename)
        self.mode = mode
        self.max_readers = max_readers
        if self.mode == "threads":
            self.semaphore = threading.Semaphore(max_readers)
            self.write_lock = threading.Lock()
            self.read_lock = threading.Lock()
            self.lock_for_taking_semaphore = threading.Lock()
        else:
            self.semaphore = multiprocessing.Semaphore(max_readers)
            self.write_lock = multiprocessing.Lock()
            self.read_lock = multiprocessing.Lock()
            self.lock_for_taking_semaphore = multiprocessing.Lock()

        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    def acquire_read_lock(self):
        """
        Acquires the read lock, allowing multiple readers to read together.
        It blocks if the max number of readers is above 10
        """
        with self.lock_for_taking_semaphore:
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
        with self.lock_for_taking_semaphore:
            count = 0
            while count < self.max_readers:
                self.semaphore.acquire()
                count += 1
                logging.debug(count)
            self.write_lock.acquire()

    def release_write_lock(self):
        """
        realise the semaphores and the write lock
        :return:
        """
        for i in range(self.max_readers):
            self.semaphore.release()
        self.write_lock.release()

    def set_value(self, key, value):
        logging.debug("writer is waiting")
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
            self.release_read_lock()
            logging.debug(f"Read value: {value}")
            return value

    def delete_value(self, key):
        self.acquire_write_lock()
        result = False
        try:
            result = super().delete_value(key)
        finally:
            self.release_write_lock()
            return result







