from database import Database
from synchronized_database import SynchronizedDatabase
import threading


def test_simple_write_permission(db, key, value):
    def writer(key1, value1):
        db.set_value(key1, value1)
        print("Write completed.")

    writer_thread = threading.Thread(target=writer, args=(key, value))
    writer_thread.start()
    writer_thread.join()

    assert db.get_value(key) == value



def test_simple_read_permission(db, key):
    def reader(key1):
        value = db.get_value(key1)
        print(f"Read value: {value}")

    reader_thread = threading.Thread(target=reader, args=(key,))
    reader_thread.start()
    reader_thread.join()



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


def test_read_blocked_by_write(db, key1, value1, key2):
    def writer(key, value):
        print("Writer started.")
        db.set_value(key, value)
        print("Writer finished.")

    def reader(key):
        print("Reader waiting.")
        value = db.get_value(key)
        print(f"Reader finished, Value: {value}")

    writer_thread = threading.Thread(target=writer, args=(key1, value1))
    reader_thread = threading.Thread(target=reader, args=(key2,))

    writer_thread.start()
    reader_thread.start()

    writer_thread.join()
    reader_thread.join()


def test_multiple_readers(db):
    lock = threading.Lock()
    def reader():
        value = db.get_value("key5")
        with lock:
            print(f"Reader finished, value is {value}")

    readers = []
    for i in range(10):
        readers_thread = threading.Thread(target=reader)
        readers.append(readers_thread)

    for reader_thread in readers:
        reader_thread.start()

    for reader_thread in readers:
        reader_thread.join()


def test_readers_then_writer_then_reader(db):
    db.set_value("key", "value")

    def reader():
        value = db.get_value("key")
        print(f"Reader got value: {value}")

    def writer():
        print("Writer waiting.")
        db.set_value("key", "new_value")
        print("Writer finished.")

    readers = []
    for i in range(5):
        readers_thread = threading.Thread(target=reader)
        readers.append(readers_thread)

    writer_thread = threading.Thread(target=writer)
    reader_thread2 = threading.Thread(target=reader)

    for reader_thread in readers:
        reader_thread.start()

    writer_thread.start()
    reader_thread2.start()

    for reader_thread in readers:
        reader_thread.join()

    writer_thread.join()
    reader_thread2.join()






def main():
    db = SynchronizedDatabase('database.pkl', "threads")

    # קבלת הרשאת כתיבה כאשר אין תחרות
    #test_simple_write_permission(db, "name", "daniel")

    # קבלת הרשאת קריאה כשאין תחרות
    #db.set_value("name", "daniel")
    #test_simple_read_permission(db, "name")

    #   חסימת הרשאת כתיבה כאשר מישהו קורה
    #db.set_value("name", "daniel")
    #test_write_blocked_by_read(db, "name", "key2", "value2") # add time.sleep(2) in get value

    # חסימת הרשאת קריאה כאשר מישהו כותב
    #test_read_blocked_by_write(db, "key1", "value1", "name")

    # עשרה קוראים במקביל
    #db.set_value("key5", "value5")
    #test_multiple_readers(db)

    #חסימת הרשאת כתיבה לכותב כאשר יש קוראים, חסימת הרשאת קריאה לקוראים כאשר אותו כותב עובד
    test_readers_then_writer_then_reader(db)











if __name__ == '__main__':
    main()