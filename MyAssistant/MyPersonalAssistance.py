from . import ABook


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
def add_contact(args: list[str], contacts: ABook.AddressBook) -> str:
    if len(args) != 2:
        raise IndexError("Invalid number of arguments. Expecting NAME and PHONE.")
    name, phone = args

    if contacts.find(name):
        raise KeyError("Contact already exists.")

    new_record = ABook.Record(name)
    new_record.add_phone(phone)
    contacts.add_record(new_record)
    return f"Contact '{name}' added."


@input_error
def change_contact(args: list[str], contacts: ABook.AddressBook) -> str:
    if len(args) != 2:
        raise ValueError("Invalid number of arguments. Expecting NAME and PHONE.")
    name, phone = args
    record = contacts.find(name)
    if not record:
        raise KeyError(f"Contact '{name}' not found.")
    try:
        contacts.change_phone(name, record.phones[0].value, phone)

    except ValueError:
        raise ValueError(f"Invalid phone number: {phone}")
    return f"Contact '{name}' updated."


@input_error
def show_phone(args: list[str], contacts: ABook.AddressBook) -> str:
    if len(args) != 1:
        raise IndexError("Invalid number of arguments. Expecting NAME.")
    name = args[0]
    if not contacts:
        raise ValueError("Contacts not found.")
    record = contacts.find(name)
    if not record:
        raise KeyError(f"Contact '{name}' not found.")
    return record


def show_all(contacts: ABook.AddressBook) -> str:
    if not contacts.data:
        return "No contacts found."
    return "\n".join(f"{record}" for record in contacts.data.values())


@input_error
def addbirthday(args: list[str], contacts: ABook.AddressBook) -> str:    
    if len(args) != 2:
        raise IndexError("Invalid number of arguments. Expecting NAME and BIRTHDAY.")
    name, birthday = args
    if not contacts.find(name):
        raise KeyError(f"Contact '{name}' not found.")

    try:
        contacts.update_birthday(name,birthday)
    except ValueError:
        raise ValueError(f"Inccorrect date value => {birthday} except YYYY.MM.DD")
    return f"Contact '{name}' updated."

@input_error
def birthdays(contacts: ABook.AddressBook) -> str:
    return contacts.get_upcoming_birthdays()

def parse_input(user_input: str) -> tuple[str, ...]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    if cmd not in __commands__:
        raise ValueError(f"Invalid command. Use the following commands: {', '.join(__commands__)}")
    return cmd, *args


def main():
    contacts = ABook.AddressBook()
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
            print(addbirthday(args,contacts))
        elif command == "show-birthday":
            # реалізація
            pass
        elif command == "birthdays":            
            print(birthdays(contacts))
        elif command == "help":
            print(f"Use the following commands: {', '.join(__commands__)}")


if __name__ == "__main__":
    main()
