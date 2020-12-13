from HelperLibrary.Validator import Validator
from Interface.SettingsCommandLineInterface import CLI as SettingsCLI
from BookingSystem.Book import Book
from BookingSystem.Information import Information


class BookMenuItem:
    def __init__(self, singleton):
        self.singleton = singleton

    def execute(self):
        if Validator("book").should_continue():
            result = Book(self.singleton.name).initiate_booking()
            print(result)

    def exit_initiated(self):
        pass


class SettingsMenuItem:
    def __init__(self, singleton):
        self.singleton = singleton
        self.is_exit_initiated = False

    def execute(self):
        user_deleted = SettingsCLI(self.singleton).initiate()
        if user_deleted:
            self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class LogoutMenuItem:
    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Logging out...")
        self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class InformationMenuItem:
    def __init__(self, singleton):
        self.username = singleton.name

    def execute(self):
        if Validator("information").should_continue():
            Information(self.username).execute()

    def exit_initiated(self):
        pass


class CLI:
    def __init__(self, singleton):
        self.main_menu_dictionary = {
            "b": BookMenuItem(singleton),
            "i": InformationMenuItem(singleton),
            "s": SettingsMenuItem(singleton),
            "l": LogoutMenuItem()
        }

    def initiate(self):
        exit_initiated = False
        while not exit_initiated:
            choice = input("Enter b to book a drone, i to get booking information, s for settings and l to logout:")
            menu_item = self.main_menu_dictionary.get(choice)
            if menu_item is None:
                print("Please enter valid choice")
                continue
            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()
