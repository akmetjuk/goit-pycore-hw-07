from MyAssistant import MyPersonalAssistance as MPA
from MyAssistant import ABook

if __name__ == "__main__":

    # Створення нової адресної книги
    book = ABook.AddressBook()

    # Створення запису для John
    john_record = ABook.Record("John")
    john_record.add_phone("0123456789")
    john_record.add_phone("0555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = ABook.Record("Jane")
    jane_record.add_phone("0987654321")
    book.add_record(jane_record)

    # Створення та додавання нового запису для Taras
    taras_record = ABook.Record("Taras")
    book.add_record(taras_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("0123456789", "0111222333")

    print(john)  # Виведення: Contact name: John, phones: 0111222333; 0555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("0555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 0555555555

    book.update_birthday("John", "25.02.1990")
    book.update_birthday("Jane", "27.02.1992")

    records = book.get_upcoming_birthdays()
    if not records:
        print("No upcoming birthdays next 7 days.")
    else:
        print("Upcoming birthdays in next 7 days:")
        print("\n".join(f"Contact '{record.name}' has birthday on {record.birthday}." for record in records))

    # Видалення запису Jane
    book.delete("Jane")

    # Виведення всіх записів у книзі, що залишилися після видалення
    for name, record in book.data.items():
        print(record)

    print("\n--- Running Assistant Bot ---\n")
    assistant = MPA.main()
