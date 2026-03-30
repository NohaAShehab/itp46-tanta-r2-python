
######################### define global variable

course_name = 'python'

print(course_name)

course_name = 'Introduction to Python'
print(course_name)


##################### local variable ,define in function ?

def display_info():
    username = input('Please enter your name: ') # local variable, can be accessed only inside the fun.
    print(f"username: {username}")

# display_info()
# print(username)  # username is local for display_info


###########################################
### access global variable from inside the function
""" 1- read/print global variable """
def print_course():
    print(f"course name: {course_name}")

# print_course()


"""2- update value of global variable from inside the function  """

def modify_course():
    """ please don't create new local variable , use the global variable """
    global course_name
    course_name = input('Please enter course name: ')
    print(f" course name: {course_name}")

# modify_course()
# print(course_name)


""" 3- we may define function inside a function ?"""

def outer_function():
    content  = "Scoping, modules, packages, exception handling, files" # local variable
    """ local variable can be accessed any where in the function, inner functions, 
    can access it. """

    def display_content():
        print(f"Today's content is {content}")

    display_content()


# outer_function()

""" case 02 ??"""

def outer_function():
    content = "Scoping, modules, packages, exception handling, files" # local variable for the outer

    def update_content():
        content = input('Please enter course name: ') # new local variable
        print(f"content = {content}")
    update_content()

    print(f"after update content is {content}")

# outer_function()

""" update local variable  from inside inner function """
def outer_function3():
    content = "Scoping, modules, packages, exception handling, files"

    def update_content():
        # please don't create new local variable , please use the parent's local one ?
        nonlocal content
        content = input('Please enter updated content : ')
        print(f"content = {content}")

    print(f"before calling update_content : {content}")
    update_content()
    print(f"after update content is {content}")

# outer_function3()

#####################################



# def abc():
#
#     print("--- hello")
#     def test():
#         nonlocal  username
#         username = 'updated'
#         print(username)
#     test()
#     print(username)
# abc()  #syntax error

###############################################

def test_function():
    print("hello from test function")
    def update_track():
        global track  # if global variable doesn't exists, will create. it
        track = input('Please enter track name: ')
        print(f"track = {track}")

    update_track()

test_function()
print(track)
































