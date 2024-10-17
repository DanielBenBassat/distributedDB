from database import Database






def main():
    my_dict_obj = Database()

    # הוספת ערכים
    print(my_dict_obj.set_value("name", "Alice"))
    print(my_dict_obj.set_value("age", 30))

    my_dict_obj.print_dict()
    print(my_dict_obj.delete_value("age"))
    my_dict_obj.print_dict()


if __name__ == '__main__':
    main()