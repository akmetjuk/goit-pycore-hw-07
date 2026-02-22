from . import abook 


__commands__ = ["hello", "add", "change", "phone", "add-birthday", "show-birthday", "birthdays", "help", "all", "close", "exit"]


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {e}"
        except KeyError as e:
            return f"Key error: {e}"
        except IndexError:
            return "Enter the argument for the command"
    return inner


@input_error
def add_contact(args: list[str], contacts: abook.AddressBook) -> str:
    if len(args) < 1:
        raise IndexError("Invalid number of arguments. Expecting at least NAME. You also can add PHONE.")
    name:str = args[0]
    phone:str = None
    if len(args) > 1:
        phone = args[1]
    if contacts.find(name):
        if phone:
            contacts.change_phone(name, phone)
    else:
        new_record = abook.Record(name)
        if phone:
            new_record.add_phone(phone)
        contacts.add_record(new_record)
    return f"Contact '{name}' updated with phone '{phone}'." if phone else f"Contact '{name}' added without phone."


@input_error
def change_contact(args: list[str], contacts: abook.AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Invalid number of arguments. Expecting NAME and PHONE.")
    name, phone = args
    record:abook.Record = contacts.find(name)
    if not record:
        raise KeyError(f"Contact '{name}' not found.")
    try:
        contacts.change_phone(name, phone, record.phones[0].value if record.phones else None)
    except ValueError as e:
        raise ValueError(f"Invalid phone number: {phone}. Error: {e}")
    return f"Contact '{name}' updated with new phone '{phone}'."


@input_error
def show_phone(args: list[str], contacts: abook.AddressBook) -> str:
    if len(args) != 1:
        raise IndexError("Invalid number of arguments. Expecting NAME.")
    name:str = args[0]
    if not contacts:
        raise ValueError("Contacts not found.")
    record:abook.Record = contacts.find(name)
    if not record:
        raise KeyError(f"Contact '{name}' not found.")
    return record


def show_all(contacts: abook.AddressBook) -> str:
    if not contacts.data:
        return "No contacts found."
    return "\n".join(f"{record}" for record in contacts.data.values())


@input_error
def add_birthday(args: list[str], contacts: abook.AddressBook) -> str:
    if len(args) != 2:
        raise IndexError("Invalid number of arguments. Expecting NAME and BIRTHDAY.")
    name, birthday = args
    if not contacts.find(name):
        raise KeyError(f"Contact '{name}' not found.")
    try:
        contacts.update_birthday(name, birthday)
    except ValueError as e:
        raise ValueError(e)
    return f"Contact '{name}' updated with birthday '{birthday}'."


@input_error
def show_birthday(args: list[str], contacts: abook.AddressBook) -> str:
    if len(args) != 1:
        raise IndexError("Invalid number of arguments. Expecting NAME.")
    name:str = args[0]
    record:abook.Record = contacts.find(name)
    if not record:
        raise KeyError(f"Contact '{name}' not found.")
    if not record.birthday:
        raise ValueError(f"Contact '{name}' has no birthday.")
    return f"Contact '{name}' has birthday on {record.birthday.value.strftime('%d.%m.%Y')}."


@input_error
def birthdays(contacts: abook.AddressBook) -> str:
    bdays: list[abook.Record] = contacts.get_upcoming_birthdays()
    if not bdays:
        return "No upcoming birthdays next 7 days."
    return "\n".join(f"Contact '{record.name.value}' has birthday on {record.birthday.value.strftime('%d.%m.%Y')}." for record in bdays)


def parse_input(user_input: str) -> tuple[str, ...]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    if cmd not in __commands__:
        raise ValueError(f"Invalid command. Use the following commands: {', '.join(__commands__)}")
    return cmd, *args


def main():
    contacts = abook.AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")

        try:
            command, *args = parse_input(user_input)
        except ValueError as e:
            print(e)
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        elif command == "help":
            print(f"Use the following commands: {', '.join(__commands__)}")


if __name__ == "__main__":
    main()
