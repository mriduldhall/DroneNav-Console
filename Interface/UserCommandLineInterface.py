from HelperLibrary.Validator import Validator
from HelperLibrary.SlowPrint import slowprint
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


class HelpMenuItem:
    def __init__(self):
        pass

    @staticmethod
    def execute():
        slowprint("Welcome to DroneNav help\n")
        slowprint("We will talk about each of the available menus available to you after you log in\n\n")
        slowprint("Let's begin with the booking menu. You can access this menu by entering b from the main menu.\n")
        slowprint("In the booking menu you are asked the name of the origin city and the destination city.\nMake sure you enter the name and not the number\n")
        slowprint("After this you are sent a message saying booking successful and your drone's number if you're booking was successful.\n")
        slowprint("However if a drone is not available a message is sent asking you to try again later.\n\n")
        slowprint("The information menu is next.\n")
        slowprint("You can access this menu by entering i from the main menu.\n")
        slowprint("From the information menu you can get the information of your current active booking including the drone's number, origin and destination.\n\n")
        slowprint("The final menu is settings.\n")
        slowprint("This menu is accessed by entering s from the menu.\n")
        slowprint("You can change your password and delete your account from here.\n\n")

    def exit_initiated(self):
        pass


class CLI:
    def __init__(self, singleton):
        self.main_menu_dictionary = {
            "b": BookMenuItem(singleton),
            "i": InformationMenuItem(singleton),
            "s": SettingsMenuItem(singleton),
            "h": HelpMenuItem(),
            "l": LogoutMenuItem()
        }

    def initiate(self):
        exit_initiated = False
        while not exit_initiated:
            choice = input("Enter b to book a drone, i to get booking information, s for settings, h for help and l to logout:")
            menu_item = self.main_menu_dictionary.get(choice)
            if menu_item is None:
                print("Please enter valid choice")
                continue
            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()
