""" create, use python modules, packages """
""""""
"""1-  module ---> I need to import the module ?? """
# import  inputs_module
#
# numm = inputs_module.ask_for_int("please enter age: ")
# print(numm)

"""2-  alias module name """
# import inputs_module as my_inputs
# name =  my_inputs.ask_for_alpha("Please enter name")
# print(name)


"""3- import module from package ?"""
#
# import  iti.math_ops
#
# res = iti.math_ops.sum_num(3,4)
# print(res)

# import  iti.math_ops as my_math
#
# print(my_math.sum_num(34,5))


""" import block from module/ package """

# from inputs_module import msg
#
# # print(msg)
#
# from iti.math_ops import pii
#
# from iti.math_ops import sum_num  as my_num
# print(my_num(34,5))



""" check this """
# import  inputs_module

# username = inputs_module.ask_for_alpha("Please enter your username: ")


# print(inputs_module.__name__)
""" ====================="""
# from demos.validators import validate_num
#
# print(validate_num(10.23))

# import iti.math_ops
# import demos.validators


# print(iti.math_ops.sum_num(3,4))

from demos import validate_string_value



