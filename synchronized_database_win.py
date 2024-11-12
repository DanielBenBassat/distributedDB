from file_database import FileDatabase
from pywin32_file import FileDatabaseWin
import os
import logging
import time
import win32event
import win32api
import win32file

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/synchronized.log'


class SynchronizedDatabase(FileDatabaseWin):
    def __init__(self, filename, mode, max_readers=10):
        """
        Initialize synchronized database that inherits from FileDatabase, creates locks and semaphore according to mode
        :param filename: file name
        :param mode: threads or multiprocessing
        :param max_readers: max number of simultaneous readers
        """
        super().__init__(filename)
        self.mode = mode
        self.max_readers = max_readers
        self.available_semaphore_taking = True

        # Create synchronization mechanisms using pywin32
        # Event, Mutex, and Semaphore from win32
        self.event = win32event.CreateEvent(None, 0, 0, None)  # Event (manual reset, non-signaled initially)
        self.mutex = win32event.CreateMutex(None, False, None)  # Mutex (non-owned initially)
        self.semaphore_handle = win32file.CreateSemaphore(None, 0, max_readers, None)  # Semaphore

        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    def acquire_read_lock(self):
        """
        Acquires the read lock, allowing multiple readers to read together.
        It blocks if the max number of readers is above 10
        """
        while not self.available_semaphore_taking:
            time.sleep(0.01)  # Let other threads check the flag periodically

        # Wait for the semaphore to allow a reader
        win32event.WaitForSingleObject(self.semaphore_handle, win32event.INFINITE)
        logging.debug("Reader acquired semaphore")

        # No need for additional read lock in this case as it's already controlled by semaphore
        logging.debug("Reader can access database now")

    def release_read_lock(self):
        """
        Releases the read lock, decrementing the semaphore to allow other readers or writers.
        """
        # Release the semaphore to allow others to read
        win32file.ReleaseSemaphore(self.semaphore_handle, 1)
        logging.debug("Reader released semaphore")

    def acquire_write_lock(self):
        """
        Acquires the write lock by first acquiring the mutex and taking all semaphores.
        """
        while True:
            # First acquire the mutex (ensures only one writer can acquire at a time)
            result = win32event.WaitForSingleObject(self.mutex, win32event.INFINITE)
            if result == win32event.WAIT_OBJECT_0:
                logging.debug("Writer acquired mutex")

                # Lock for reading operations (simulating the concept of taking all semaphores)
                for _ in range(self.max_readers):
                    win32event.WaitForSingleObject(self.semaphore_handle, win32event.INFINITE)
                logging.debug("All semaphores acquired by writer")

                return

    def release_write_lock(self):
        """
        Releases the write lock and all semaphores, and resets the available_semaphore_taking flag.
        """
        # Release all the semaphores
        for _ in range(self.max_readers):
            win32file.ReleaseSemaphore(self.semaphore_handle, 1)
        logging.debug("Writer released all semaphores")

        # Release the mutex after write completion
        win32event.ReleaseMutex(self.mutex)
        logging.debug("Writer released mutex")

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
