from multiprocessing import Process
#from synchronized_database import SynchronizedDatabase
from synchronized_database_win import SynchronizedDatabase


def writer(db, key, value):
    print("writer waiting")
    db.set_value(key, value)
    print('Write completed.')


def reader(db, key):
    value = db.get_value(key)
    print(f"Read value: {value} for {key}")


def test_simple_write_permission(db, key, value):
    writer_process = Process(target=writer, args=(db, key, value,))
    writer_process.start()
    writer_process.join()

    print("Test 1: Simple write permission passed.")


def test_simple_read_permission(db, key):
    reader_process = Process(target=reader, args=(db, key,))
    reader_process.start()
    reader_process.join()
    print("Test 2: Simple read permission passed.")


def test_write_blocked_by_read(db,key1, key2, value2):

    reader_process = Process(target=reader, args=(db,key1,))
    writer_process = Process(target=writer, args=(db,key2, value2))

    reader_process.start()
    writer_process.start()

    reader_process.join()
    writer_process.join()


def test_read_blocked_by_write(db,key1, value1, key2):

    writer_process = Process(target=writer, args=(db, key1, value1))
    reader_process = Process(target=reader, args=(db, key2,))

    writer_process.start()
    reader_process.start()

    writer_process.join()
    reader_process.join()

    print("Test 4: Read blocked by write passed.")


def test_multiple_readers(db, key):
    readers = []
    for i in range(10):
        reader_process = Process(target=reader, args=(db, key,))
        readers.append(reader_process)

    for reader_process in readers:
        reader_process.start()

    for reader_process in readers:
        reader_process.join()

    print("Test 5: Multiple readers passed.")


def test_readers_then_writer_then_reader(db, key, value, new_value):
    db.set_value(key, value)
    readers = []
    for i in range(5):
        reader_process = Process(target=reader, args=(db, key,))
        readers.append(reader_process)

    writer_process = Process(target=writer, args=(db, key, new_value,))
    reader_process2 = Process(target=reader, args=(db, key,))

    for reader_process in readers:
        reader_process.start()

    writer_process.start()
    reader_process2.start()

    for reader_process in readers:
        reader_process.join()

    writer_process.join()
    reader_process2.join()


def main():
    db_main = SynchronizedDatabase('database.pkl', "process")

    #test_simple_write_permission(db_main, "name", "daniel")

    #test_simple_read_permission(db_main, "name")

    #test_write_blocked_by_read(db_main, "name", "key2", "value2") # add time.sleep(2) in get value

    #test_read_blocked_by_write(db_main, "key1", "value1", "name")

    #test_multiple_readers(db_main, "name")

    test_readers_then_writer_then_reader(db_main, "name", "daniel", "dani")


if __name__ == "__main__":
    main()
