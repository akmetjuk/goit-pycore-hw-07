from collections import UserDict
from datetime import datetime, timedelta
from colorama import init, Fore
import re


def normalize_phone(phone_number: str) -> str:
    """Нормалізувати номер телефону та додати префікс +38.

    Args:
        phone_number: Телефонний номер з будь-якими символами

    Returns:
        Нормалізований номер у форматі +38XXXXXXXXXX

    Raises:
        ValueError: Якщо не вдалося виділити 10-значний номер
    """
    pattern = r'\d+'
    ph = ''.join(re.findall(pattern, phone_number))
    if len(ph) == 9:
        ph = '380' + ph
    if len(ph) == 10 and ph.startswith('0'):
        ph = '38' + ph
    if len(ph) != 12:
        raise ValueError(f'unable to extract phone number => {phone_number}')
    return f"+{ph}"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError(f"Invalid date format ({value}). Use DD.MM.YYYY")


class Phone(Field):
    def __init__(self, value):
        super().__init__(normalize_phone(value))

    def change_phone(self, value):
        self.value = normalize_phone(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        init(autoreset=True)
        return f"Contact name: {Fore.BLUE}{self.name.value}{Fore.RESET}, phones: {Fore.GREEN}{'; '.join(p.value for p in self.phones)}{Fore.RESET}"

    def find_phone(self, phone: str) -> Phone | None:
        """
        Пошук телефону в записі.
        Args:
            phone: Номер телефону для пошуку
        Returns:
            Знайдений об'єкт Phone або None, якщо не знайдено
        """
        try:
            phone = normalize_phone(phone)
            for p in self.phones:
                if p.value == phone:
                    return p
        except:
            return None

    def add_phone(self, phone: str):
        """
        Додайте новий номер телефону до запису, якщо такого номеру не ще немає.
        Args:
            phone: Номер телефону для додавання
        """
        try:
            if self.find_phone(phone) is None:
                self.phones.append(Phone(phone))
        except:
            pass

    def update_birthday(self, bday: str):
        """Додає або змінює дату народження 
        Args:
            bday: Дата у форматі 'DD.MM.YYYY' 
        Raises:
            ValueError: Якщо формат дати невірний
        """        
        try:
            birthday = Birthday(bday)
            if birthday:
                if birthday.value:
                    self.birthday = birthday
        except ValueError as e:
            raise ValueError(e)

    def edit_phone(self, current_phone: str, new_phone: str):
        """"
        Змінити існуючий номер телефону на новий.
        Args:
            current_phone: Поточний номер телефону для заміни
            new_phone: Новий номер телефону
        """
        try:
            p = self.find_phone(current_phone)
            if p:
                p.change_phone(new_phone)
        except:
            pass

    def remove_phone(self, phone: str):
        try:
            self.phones.remove(self.find_phone(phone))
        except:
            pass


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

        
    def get_upcoming_birthdays(self) -> str:
        """Отримати список користувачів з днями народження на наступному тижні.
        Args:
            users: Список словників з ключами 'name' та 'birthday' (формат 'DD.MM.YYYY')
        Returns:
            Перелік співробітник з днями народження
        """
        today = datetime.today().date()

        upcoming = list()
        for record in self.data.values():
            if not record.birthday:
                continue
            birthday = record.birthday.value.replace(year=today.year).date()

            # Якщо день народження вже минув цього року, розглядаємо наступний рік
            if birthday < today:
                birthday = birthday.replace(year=birthday.year + 1)

            days_between = birthday.toordinal() - today.toordinal()
            # Розглядаємо дні народження на наступні 7 днів
            if days_between > 7:
                continue

            # Якщо день народження на вихідний, переносимо на понеділок
            weekday = birthday.weekday()
            if weekday > 4:
                birthday = birthday + timedelta(days=(7 - weekday))

            upcoming.append(f"Contact '{record.name.value}' has birthday on {record.birthday.value.strftime('%d.%m.%Y')}.")

        return upcoming 

    def add_record(self, record: Record):
        """Додайте запис до адресної книги.
        Args:
            record: Об'єкт Record для додавання
        Raises:
            IndexError: Якщо контакт з таким ім'ям вже існує
        """
        n = str.lower(record.name.value).strip()
        r = self.find(n)
        if r:
            raise IndexError(f"Contact '{record.name.value}' already exists.")
        self.data[n] = record

    def find(self, name: str) -> Record | None:
        """
        Знаходить запис за ім'ям.
        Args:
            name: Ім'я контакту для пошуку
        Returns:
            Знайдений об'єкт Record або None, якщо не знайдено
        """
        return self.data.get(str.lower(name).strip())

    def change_phone(self, name: str, current_phone: str, new_phone: str):
        """Змінює номер телефону для існуючого контакту.
        Args:
            name: Ім'я контакту для зміни
            current_phone: Поточний номер телефону для заміни
            new_phone: Новий номер телефону
        Raises:
            KeyError: Якщо контакт з таким ім'ям не знайдено
            ValueError: Якщо поточний номер телефону не знайдено в записі контакту
        """
        record = self.find(name)
        if not record:
            raise KeyError(f"Contact '{name}' not found.")
        if not record.find_phone(current_phone):
            raise ValueError(f"Phone '{current_phone}' not found for contact '{name}'.")
        record.edit_phone(current_phone, new_phone)

    def update_birthday(self, name: str, birthday: str):        
        record = self.find(name)
        if not record:
            raise KeyError(f"Contact '{name}' not found.")
        record.update_birthday(birthday)

    def delete(self, name: str):
        """Видаляє запис з адресної книги за ім'ям.
        Args:
            name: Ім'я контакту для видалення
        Raises:
            KeyError: Якщо контакт з таким ім'ям не знайдено
        """
        self.data.pop(str.lower(name).strip())
