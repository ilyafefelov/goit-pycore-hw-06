from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone_number):
        if not re.fullmatch(r'\d{10}', phone_number):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(phone_number)


class Record:
    def __init__(self, name, phones=None):
        self.name = Name(name)
        self.phones = phones if phones else []

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if new_phone in self.phones:
            return f"Phone {phone} already exists for {self.name.value}."
        self.phones.append(new_phone)
        return f"Phone {phone} added to {self.name.value}."

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return f"Phone {phone} removed."
        raise ValueError("Phone not found.")

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return f"Phone {old_phone} changed to {new_phone}."
        raise ValueError("Old phone not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError("Phone not found.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            existing_record = self.data[record.name.value]
            existing_record.phones.extend(record.phones)
            return f"Record for {record.name.value} already exists. Phone numbers combined."
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        raise KeyError(f"Record for {name} not found.")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record for {name} deleted."
        raise KeyError(f"Record for {name} not found.")