from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Birthday must be in format DD-MM-YYYY.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError('Phone number not found.')
    

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ", ".join(str(p) for p in self.phones)
        birthday = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"{self.name.value}: {phones}{birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, KeyError) as e:
            return f"Error: {str(e)}"

    return wrapper


@input_error
def add_contact(args, book):
    if len(args) < 2:
        return "Not enough arguments. Usage: add <name> <phone>"
    name, phone = args[0], args[1]
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return f"Contact {name} added/updated with phone {phone}."


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Not enough arguments. Usage: add-birthday <name> <DD-MM-YYYY>"
    name, birthday = args[0], args[1]
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(birthday)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book):
    if len(args) < 1:
        return "Not enough arguments. Usage: show-birthday <name>"
    name = args[0]
    record = book.find(name)
    if not record or not record.birthday:
        return "Birthday not found."
    return f"{name}'s birthday: {record.birthday.value}"


def birthdays(book):
    if not book.data:
        return "No contacts in the book."
    return "\n".join(f"{name}: {record.birthday.value}" for name, record in book.data.items() if record.birthday)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue
        parts = user_input.split(maxsplit=2)
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print("Change command not implemented yet.")
        elif command == "phone":
            print("Phone command not implemented yet.")
        elif command == "all":
            print(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()