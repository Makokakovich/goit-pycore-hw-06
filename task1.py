from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        # перевірка формату номера
        if not self.is_valid_phone(value):
            raise ValueError("Phone must be 10 digits")
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return isinstance(value, str) and value.isdigit() and len(value) == 10


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        target = self.find_phone(phone)
        if target is None:
            raise ValueError("Phone not found")
        self.phones.remove(target)

    def edit_phone(self, old_phone, new_phone):
        # шукаємо номер, який треба замінити
        target = self.find_phone(old_phone)
        if target is None:
            raise ValueError("Phone not found")
        new_phone_obj = Phone(new_phone)
        target.value = new_phone_obj.value

    def find_phone(self, phone):
        for found in self.phones:
            if found.value == phone:
                return found
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        # ключем запису є ім'я контакту
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for _, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")
