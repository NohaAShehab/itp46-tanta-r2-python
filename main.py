def div_nums():
    try:
        num1 = int(input("Enter a number: "))
        num2 = int(input("Enter a number: "))
        res = num1 / num2
    except Exception as e:
        print("---- error ----")
        print(e)
        return  math.nan
    else:
        print("----success---")
        print(f"num1 = {num1}, num2 = {num2}, res = {res}")
        return res
    finally:
        # finally execution preceed return
        print("-----thank you for using this function")
    print("------**************************")


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
