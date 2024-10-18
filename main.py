from database import Database
from synchronized_database import SynchronizedDatabase
from threading import Lock, Semaphore
import threading
import time
semaphore = Semaphore(10)

def acquire_write_lock():
    count = 0
    while count < 10:
        semaphore.acquire()
        count += 1
        print(count)


def handle_clinet():
    semaphore.acquire()
    time.sleep(5)
    semaphore.release()



def main():
    my_dict_obj = SynchronizedDatabase()

    for i in range(1):
        thread = threading.Thread(target= handle_clinet, args=())
        thread.start()

    thread = threading.Thread(target=acquire_write_lock(), args=())
    thread.start()







if __name__ == '__main__':
    main()