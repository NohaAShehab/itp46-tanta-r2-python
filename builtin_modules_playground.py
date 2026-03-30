
import  math
#
# print(math.pi)
#
# print(math.ceil(333.33))


# import random
#
# print(random.randint(1,100))


import re  # regex --> regular expression
import sys

# pattern  =r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
pattern =r'[A-Za-z0-9]+@[\w]+\.[\w]+'
email = "noha@gmail.com"


valid = re.match(pattern, email)
print(valid, "first email", email)



email2 = 'noha@gmail.com@iti.com'
""" match function return with match object if the first part of the
string matches pattern """
valid2 = re.match(pattern, email2)
print(valid2, 'second email', email2)


""" some of the patterns ----> not covered all the cases """

# use function matchall ?
email3 = 'noha@gmail.comm@iti.gov'
valid3 = re.fullmatch(pattern, email3)
print(valid3, 'third email', email3)


""" sys , os """

print(sys.path)
num = 10
print(sys.getsizeof(num))

name = ''
print(sys.getsizeof(name))

""" datetime """
import datetime
print(datetime.datetime.now())
# convert string to datatime object and vice..