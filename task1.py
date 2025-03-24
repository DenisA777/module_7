from collections import UserDict
from datetime import datetime, timedelta

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments provided."
        except ValueError as e:
            return f"Value error: {e}"
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return f"Error: {e}"
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        if self.value > datetime.now():
            raise ValueError("Date of birth cannot be in the future")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def edit_phone(self, old_phone, new_phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
    
    def __str__(self):
        phones_str = ", ".join(p.value for p in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "Not set"
        return f"{self.name.value}: Phones: {phones_str}, Birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def search_by_name(self, name):
        return self.data.get(name)
    
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now()
        week_later = today + timedelta(days=7)
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= week_later:
                    if birthday_this_year.weekday() in [5, 6]:
                        birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))
                    upcoming_birthdays.append({"name": record.name.value, "birthday": birthday_this_year.strftime("%d.%m.%Y")})
        return upcoming_birthdays

@input_error
def add_contact(args, book):
    if len(args) < 2:
        return "Not enough arguments."
    name, phone = args[0], args[1]
    record = book.search_by_name(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return f"Contact {name} added/updated with phone {phone}."

@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Not enough arguments."
    name, birthday = args[0], args[1]
    record = book.search_by_name(name)
    if not record:
        return "Contact not found."
    record.add_birthday(birthday)
    return f"Birthday added for {name}."

@input_error
def show_birthday(args, book):
    if len(args) < 1:
        return "Not enough arguments."
    name = args[0]
    record = book.search_by_name(name)
    if not record or not record.birthday:
        return "Birthday not found."
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    return "\n".join(f"{b['name']}: {b['birthday']}" for b in upcoming) if upcoming else "No upcoming birthdays."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
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