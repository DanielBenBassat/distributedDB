from database import Database
from multiprocessing import Lock, Semaphore
from threading import Lock, Semaphore
import time

class SynchronizedDatabase(Database):
    def __init__(self, filename="database.pkl", mode="threads", max_readers=10):
        super().__init__(filename)
        self.mode = mode
        self.max_readers = max_readers
        self.semaphore = Semaphore(max_readers)
        self.readers = 0
        self.write_lock = Lock()
        self.reader_count_lock = Lock()



    def acquire_read_lock(self):
        self.semaphore.acquire()
        with self.reader_count_lock:
            self.readers += 1


    def release_read_lock(self):
        with self.reader_count_lock:
            self.readers -= 1
        self.semaphore.release()

    def acquire_write_lock(self):
        count = 0
        while count < self.max_readers:
            self.semaphore.acquire()
            count += 1
            print(count)
        self.write_lock.acquire()

    def release_write_lock(self):
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







