# import libraries
import pandas
import math


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


# Yes_no checker [recycled from MMF]
def yes_no(question):
    while True:
        response = input(question).lower()

        if response == "yes" or response == "y":
            return "yes"

        elif response == "no" or response == "n":
            return "no"

        else:
            print("Please enter yes or no")


def not_blank(question, error):
    while True:
        response = input(question)

        if response == "":
            print(f"{error}. Sorry but this cannot be blank. Please retry")

        elif response == " ":
            print(f"{error}. Sorry but this cannot be blank. PLease retry")

        else:
            return response


# currency formatting function
def currency(x):
    return "${:.2f}".format(x)


# Gets expenses, returns lists which has
# the data frame and sub-total
def get_expenses(variable_fixed):
    # set up dictionaries and lists
    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # loop to get component, quantity and price
    item_name = " "
    while item_name.lower() != "xxx":

        print()
        # get name, quantity and item
        item_name = not_blank("item name: ",
                              "the component name cannot be blank")

        if item_name.lower() == "xxx":
            break

        if variable_fixed == "variable":
            quantity = num_check("Quantity: ",
                                 "The amount must be a whole number, "
                                 "more than zero",
                                 int)
        else:
            quantity = 1

        price = num_check("How much for a single item? $",
                          "The price must be a number <more than 0>",
                          float)

        # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] \
                            * expense_frame['Price']

    # Find sub-total
    sub_total = expense_frame['Cost'].sum()

    # Currency Formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


def expense_print(heading, frame, subtotal):
    print()
    print(f"**** {heading} Costs ****")
    print(frame)
    print()
    print(f"{heading} Costs: ${subtotal:.2f}")
    return ""


def profit_goal(total_costs):
    # initialise variables and error message
    error = "Please enter a valid Profit goal\n"

    valid = False
    while not valid:

        # ask for profit goal
        response = input("What is your profit goal (eg $500 or 50%) ")

        # check if first character is $
        if response[0] == "$":
            profit_type = "$"
            # Get amount
            amount = response[1:]

        # Check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount
            amount = response[:-1]

        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # check amount is a number more than zero
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no(f"Do you mean ${amount:.2f}, ie {amount:.2f} dollars. y / n ")

            # set profit type
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no(f"Do you mean {amount}%?. y / n ")
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


# main routine goes here
# ask if user wants Instructions
want_instructions = yes_no("Do you want to read the instructions? ").lower()
if want_instructions == "yes":
    print('''\n
    * * * * Instructions * * * *
    
    First you will be inputing the final products name [example: Customized mugs]
    
    Afterwards you will be asked about what your variable expenses are 
    [name, how many and price]
    once you have entered all variable expenses type 'xxx'
    
    Then you will be asked if you have fixed costs
    if you do have fixed costs you'll be asked their name and price
    once you have entered all fixed expenses type 'xxx'
    
    you'll then be asked what you're profit goal is [example $500 or 50%]
    and what you want to round your recommended selling price to
    
    then the program will display your costs, their totals and a recommended selling price
    
    This information will also be automatically written into a text file 
          ''')
    print()

else:
    pass

# Get product name
product_name = not_blank("Product name: ", "The Product name cannot be blank")

how_many = num_check("How many items will you be producing? ",
                     "the number of items must be a whole "
                     "number more than zero", int)

print()
print("Please enter Variable costs below . . .")
# gets variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

have_fixed = yes_no("Do you have fixed costs (Yes / No)? ")

if have_fixed == "yes":
    # gets fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
else:
    fixed_sub = 0

# work out total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculate recommended price
sales_needed = all_costs + profit_target

# Ask user for rounding
round_to = num_check("Round to nearest . . .? $",
                     "Can't be 0 ", int)

# Calculate recommend price
selling_price = sales_needed / how_many
print(f"selling price (unrounded): {selling_price:.2f}")

recommended_price = round_up(selling_price, round_to)

# write data to file

#  * * * * Printing Area * * * *
print()
print(f"**** Fund Raising - {product_name} ****")
print()

expense_print("Variable", variable_frame, variable_sub)

if have_fixed == "yes":
    expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)

print()
print(f"* * * Total Costs: {all_costs:.2f}")
print()

print()
print("* * * * Profit and Sales Targets * * * *")
profit_string = f"Profit Target: ${profit_target:.2f}"
recommended_string = f"Recommended Price: ${recommended_price:.2f}"

# change frame to a string so that we can export it to file
variable_txt = pandas.DataFrame.to_string(variable_frame)
fixed_txt = pandas.DataFrame.to_string(fixed_frame)

to_write = [product_name, variable_txt, fixed_txt, profit_string, recommended_string]

# bug fixing
for item in to_write:
    print(f"{item}: {type(item)}")

# write output to file
# create file to hold data (add .txt extension)
file_name = f"{product_name}.txt"
text_file = open(file_name, "w+")

# heading
# print output
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()

# Print stuff
for item in to_write:
    print(item)
    print()
