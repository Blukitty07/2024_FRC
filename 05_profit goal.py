# functions go here


# checks that a user has enter yes / no to a cuestion
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


# main routine
all_costs = 200

# loop for quick testing
for item in range(0, 6):
    profit_target = profit_goal(all_costs)
    print(f"Profit Target : ${profit_target:.2f}")
    print(f"Total Sales: {all_costs + profit_target:.2f}")
    print()
