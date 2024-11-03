from file_database import FileDatabase
import threading
import multiprocessing
import time


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
            self.lock_for_semaphore_acquire = threading.Lock()
        else:
            self.semaphore = multiprocessing.Semaphore(max_readers)
            self.write_lock = multiprocessing.Lock()
            self.lock_for_semaphore_acquire = multiprocessing.Lock()

    def acquire_read_lock(self):
        """
        Acquires the read lock, allowing multiple readers to read together.
        It blocks if the max number of readers is above 10
        """
        with self.lock_for_semaphore_acquire:
            self.semaphore.acquire()

    def release_read_lock(self):
        """
        Releases the read lock, decrementing the semaphore to allow other readers or writers.
        """
        self.semaphore.release()

    def acquire_write_lock(self):
        """
        takes lock_for_semaphore_acquire to be the first one to take semaphoe when its realised, and then take all the semaphores until have all of them and takes the write_lock
        """
        with self.lock_for_semaphore_acquire:
            count = 0
            while count < self.max_readers:
                self.semaphore.acquire()
                count += 1
                print(count)
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
        self.acquire_write_lock()
        result = False
        try:
            result = super().set_value(key, value)
        finally:
            self.release_write_lock()
            return result

    def get_value(self, key):
        self.acquire_read_lock()
        time.sleep(2)
        value = None
        try:
            value = super().get_value(key)
        finally:
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







