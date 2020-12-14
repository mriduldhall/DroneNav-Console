from User.Login import Login
from User.Registration import Registration
from User.User import User
from HelperLibrary.Validator import Validator
from HelperLibrary.Singleton import Singleton
from HelperLibrary.SlowPrint import slowprint
from Interface.UserCommandLineInterface import CLI as UserCLI


class ExitMenuItem:

    def __init__(self):
        self.is_exit_initiated = False

    def execute(self):
        print("Exiting...")
        self.is_exit_initiated = True

    def exit_initiated(self):
        return self.is_exit_initiated


class RegisterMenuItem:

    def __init__(self):
        pass

    @staticmethod
    def exit_initiated():
        return False

    def execute(self):
        if Validator("register").should_continue():
            user = self._get_new_user_details()
            msg = Registration().register(user)
            print(msg)

        return False

    @staticmethod
    def _get_new_user_details():
        username = input("Please enter your username:")
        password = input("Please enter a password for you account:")
        return User(username, password)


class LoginMenuItem:

    def __init__(self, login_module=Login()):
        self.login_module = login_module

    @staticmethod
    def exit_initiated():
        return False

    def execute(self):
        if Validator("login").should_continue():
            logged_in = False
            try_again = True
            logged_in_username = None
            while (logged_in is False) and (try_again is True):
                username = input("Enter your username:")
                password = input("Enter your password:")

                login_result = self.login_module.validate_credentials(User(username, password))

                if login_result == Login.logged_in:
                    print("Successfully logged in")
                    logged_in = True
                    try_again = False
                    logged_in_username = username
                elif login_result == Login.does_not_exist:
                    print("Entered username does not exist")
                    valid_input = False
                    while not valid_input:
                        try:
                            try_again = bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))
                        except ValueError:
                            print("Not a valid input")
                        else:
                            valid_input = True
                else:
                    print("Incorrect username and/or password")
                    valid_input = False
                    while not valid_input:
                        try:
                            try_again = bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))
                        except ValueError:
                            print("Not a valid input")
                        else:
                            valid_input = True

            if logged_in_username is not None:
                singleton = Singleton(logged_in_username)
                UserCLI(singleton).initiate()
                singleton.reset()


class InformationMenuItem:

    def __init__(self):
        pass

    @staticmethod
    def execute():
        slowprint("DroneNav is a proof of concept app of a drone booking system based on the future of travel.\n")
        slowprint("It allows user to book drones for their travel(currently limited to the United Kingdom) for the proof of concept version.\n")
        slowprint("To emulate other users and other real world processes jobs are automatically produced for drones and speed varies for each journey.\n")
        slowprint("A drone's speed might be even slower to emulate traffic.\n")
        slowprint("Thank you for trying out DroneNav.\n")
        slowprint("""Group = ['Mridul', 'Ifaz', 'Harsh', 'Tajveer']\n""")
        slowprint("As part of the ŠŦ£∑ competition.\n")

    @staticmethod
    def exit_initiated():
        return False


class CLI:

    def __init__(self):
        self.mainmenu_dict = {
            'r': RegisterMenuItem(),
            'l': LoginMenuItem(),
            'i': InformationMenuItem(),
            'e': ExitMenuItem()
        }

    def initiate(self):
        print("Welcome to DroneNav")
        exit_initiated = False

        while not exit_initiated:
            choice = input(
                "Enter r to register an account, l to login or i to get more information.\nEnter e to exit the software.")
            menu_item = self.mainmenu_dict.get(choice)
            if menu_item is None:
                print("Enter valid choice")
                continue

            menu_item.execute()
            exit_initiated = menu_item.exit_initiated()
