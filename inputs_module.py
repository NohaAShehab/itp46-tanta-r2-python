
print("------------------------ Hello welcome to inputs module ---------")

msg = 'Hello world'

def ask_for_int(message = "input please enter a number"):
    while True:
        num = input(message)
        if num.isdigit():
            return int(num)
        else:
            print("please enter a valid number")



def ask_for_alpha(message = "input please enter a string "):
    while True:
        alpha_str = input(message)
        if alpha_str.isalpha():
            return alpha_str
        print("==== please enter a valid string ")




""" if you the code to run only when this file is run,
 entry point is this file inputs_module.py """

if __name__ == '__main__':
    salary = ask_for_int("Please enter the salary: ")
    print(f"salary: {salary}")
#
# if __name__ == "inputs_module":
#     print("---- Helllo dwwlrrwlkjrw")