# import libraries

# Functions

# Checks that an input is a float or integer > 0
def num_check(question, error, num_type):
    valid = False
    while not valid:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)
            else:
                return response

        except ValueError:
            print(error)


# main routine
get_int = num_check("how many do you need ",
                    "please enter an amount more than 0\n",
                    int)
get_cost = num_check("How much does it cost? $",
                     "Please enter a number more than 0\n",
                     float)
