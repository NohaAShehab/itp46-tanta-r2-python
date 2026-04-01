# lib , validate date, time --> size
# datetime

# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


print(isinstance(emp, object))


from abc import ABC, abstractmethod

from typing import  overload

from functools import singledispatchmethod  # overloading


class Employee:
    def __init__(self, name, email, salary):
        self.name = name
        self.email = email
        self.salary = salary

    def __str__(self):  # must return with str
        return f"{self.name}"

    def __repr__(self):  # must return with str
        return f"Employee(name={self.name}, email={self.email}, salary={self.salary})"

    def __len__(self):
        # must return with int...
        return len(self.__dict__)

    def __call__(self, *args, **kwargs):
        print("--- emp object is called ")