from pywin32_synchronized import SynchronizedDatabase
import threading


def writer(db, key, value):
    db.set_value(key, value)


def reader(db, key):
    db.get_value(key)


def test_simple_write_permission(db, key, value):
    writer_thread = threading.Thread(target=writer, args=(db, key, value))
    writer_thread.start()
    writer_thread.join()


def test_simple_read_permission(db, key):
    reader_thread = threading.Thread(target=reader, args=(db, key,))
    reader_thread.start()
    reader_thread.join()


def test_write_blocked_by_read(db, key1, key2, value2):
    reader_thread = threading.Thread(target=reader, args=(db, key1,))
    writer_thread = threading.Thread(target=writer, args=(db, key2, value2))

    reader_thread.start()
    writer_thread.start()

    reader_thread.join()
    writer_thread.join()


def test_read_blocked_by_write(db, key1, value1, key2):
    writer_thread = threading.Thread(target=writer, args=(db, key1, value1))
    reader_thread = threading.Thread(target=reader, args=(db, key2,))

    writer_thread.start()
    reader_thread.start()

    writer_thread.join()
    reader_thread.join()


def test_multiple_readers(db, key):
    readers = []
    for i in range(100):
        readers_thread = threading.Thread(target=reader, args=(db, key,))
        readers.append(readers_thread)

    for reader_thread in readers:
        reader_thread.start()

    for reader_thread in readers:
        reader_thread.join()


def test_readers_then_writer_then_reader(db, key, value, new_value):
    db.set_value(key, value)
    readers = []
    for i in range(5):
        readers_thread = threading.Thread(target=reader, args=(db, key,))
        readers.append(readers_thread)

    writer_thread = threading.Thread(target=writer, args=(db, key, new_value,))

    for reader_thread in readers:
        reader_thread.start()

    writer_thread.start()

    reader_thread2 = threading.Thread(target=reader,  args=(db, key,))

    reader_thread2.start()

    for reader_thread in readers:
        reader_thread.join()

    writer_thread.join()
    reader_thread2.join()


def main():
    db = SynchronizedDatabase('database.pkl')

    # קבלת הרשאת כתיבה כאשר אין תחרות
    #test_simple_write_permission(db, "name", "daniel")

    # קבלת הרשאת קריאה כשאין תחרות
    #db.set_value("name", "daniel")
    #test_simple_read_permission(db, "name")

    #   חסימת הרשאת כתיבה כאשר מישהו קורה
    #db.set_value("name", "daniel")
    #test_write_blocked_by_read(db, "name", "age", "17") # add time.sleep(2) in get value

    # חסימת הרשאת קריאה כאשר מישהו כותב
    #db.set_value("name", "daniel")
    #test_read_blocked_by_write(db, "key1", "value1", "name")

    # עשרה קוראים במקביל
    #db.set_value("name", "daniel")
    #test_multiple_readers(db, "name")

    #חסימת הרשאת כתיבה לכותב כאשר יש קוראים, חסימת הרשאת קריאה לקוראים כאשר אותו כותב עובד
    test_readers_then_writer_then_reader(db, "name", "daniel", "dani")











if __name__ == '__main__':
    main()