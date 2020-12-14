import time


def slowprint(string):
    for letter in string:
        print(letter, end='')
        time.sleep(0)
