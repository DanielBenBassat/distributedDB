from database import Database
from synchronized_database import SynchronizedDatabase
from threading import Lock, Semaphore
import threading
import  time


def test_simple_write_permission(db, key, value):
    def writer(key1, value1):
        db.set_value(key1, value1)
        print("Write completed.")

    writer_thread = threading.Thread(target=writer, args=(key, value))
    writer_thread.start()
    writer_thread.join()

    assert db.get_value(key) == value
    print("Test 1: Simple write permission passed.")


def test_simple_read_permission(db, key):
    def reader(key1):
        value = db.get_value(key1)
        print(f"Read value: {value}")

    reader_thread = threading.Thread(target=reader, args=(key,))
    reader_thread.start()
    reader_thread.join()

    print("Test 2: Simple read permission passed.")


def test_write_blocked_by_read(db, key1, key2, value2):

    def reader(key):
        print("Reader started.")
        db.get_value(key)
        print("Reader finished.")

    def writer(key, value):
        print("Writer waiting.")
        db.set_value(key, value)
        print("Writer finished.")

    reader_thread = threading.Thread(target=reader, args=(key1,))
    writer_thread = threading.Thread(target=writer, args=(key2, value2))

    reader_thread.start()
    writer_thread.start()

    reader_thread.join()
    writer_thread.join()

    print("Test 3: Write blocked by read passed.")

def test_read_blocked_by_write(db, key1, value1, key2):
    def writer(key, value):
        print("Writer started.")
        db.set_value(key, value)
        print("Writer finished.")

    def reader(key):
        print("Reader waiting.")
        value = db.get_value(key)
        print(f"Reader finished. Value: {value}")

    writer_thread = threading.Thread(target=writer, args=(key1, value1))
    reader_thread = threading.Thread(target=reader, args=(key2,))

    writer_thread.start()
    reader_thread.start()

    writer_thread.join()
    reader_thread.join()

    print("Test 4: Read blocked by write passed.")






def main():
    db = SynchronizedDatabase()
    # קבלת הרשאת כתיבה כאשר אין תחרות
    #test_simple_write_permission(db, "name", "daniel")
    # קבלת הרשאת קריאה כשאין תחרות
    #test_simple_read_permission(db, "name")
    #   חסימת הרשאת כתיבה כאשר מישהו קורה
    db.set_value("name", "daniel")
    #test_write_blocked_by_read(db, "name", "key2", "value2") # add time.sleep(2) in get value

    #קריאה כאשר מישהו כותב
    test_read_blocked_by_write(db, "key1", "value1", "name")











if __name__ == '__main__':
    main()