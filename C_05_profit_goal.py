# functions go here


# Checks that an answer is yes/no
def yes_no(question):

    to_check = ["yes", "no"]
    while True:

        response = input(question).lower()

        # checks that answer is yes/no
        for var_item in to_check:
            if response == var_item[0] or response == var_item:
                return var_item

        print("Please answer yes / no")


def profit_goal(total_costs):

    # Initialise variables and error message
    error = "Please enter a valid profit goal.\n"

    while True:

        # Ask for profit goal...
        response = input("what is your profit goal? (eg $500 or 50%): ")

        # check if first character is $...
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount (everything before the %)
            amount = response[:-1]

        else:
            # set amount to response for now
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than 0
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no(f"Did you mean ${amount:.2f}, ie {amount:.2f} dollars? y / n")

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no(f"Did you mean {amount}%, ie {amount} percent? y / n")

            # Set profit type based on user answer above
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal
