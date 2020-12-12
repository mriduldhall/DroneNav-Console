from User.Login import Login
from User.Registration import Registration
from User.User import User
from HelperLibrary.Validator import Validator
from HelperLibrary.Singleton import Singleton


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
                    try_again = bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))
                else:
                    print("Incorrect username and/or password")
                    try_again = bool(int(input("Would you like to try again? Enter 1 to try again and 0 to exit.")))

            if logged_in_username is not None:
                singleton = Singleton(logged_in_username)
                # teacher_CLI(singleton).initiate()
                singleton.reset()


class InformationMenuItem:

    def __init__(self):
        pass

    @staticmethod
    def execute():
        print("Currently no information available")
        return False

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
