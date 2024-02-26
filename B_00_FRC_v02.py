import pandas

# Functions go here


# Check that an int/float is more than 0
def num_check(question, error, num_type):
    while True:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)
                continue

            return response

        except ValueError:
            print(error)
            continue


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


# checks that user response is not blank
def not_blank(question, error):

    while True:
        response = input(question)

        # if response is blank, outputs error
        if response == "":
            print(f"{error} \nPlease try again.")
        else:
            return response


# currency formatting function
def currency(x):
    return f"${x:.2f}"


# Gets expenses, returns list which has the data frame and sub-total
def get_expenses(var_fixed):
    # Set up Dictionary and lists

    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # loop to get component, quantity, and price
    item_name = ""
    while item_name.lower() != "xxx":

        print()

        # Get name, quantity and item
        item_name = not_blank("Item name: ", "The component name can't be blank")
        if item_name.lower() == "xxx":
            if len(item_list) == 0:
                return "xxx"
            else:
                break

        # If quantity is fixed, set quantity to 1
        if var_fixed == "variable":
            quantity = num_check("Quantity: ", "The amount must be a whole number more than 0", int)

        else:
            quantity = 1

        price = num_check("How much for a single item? $", "The price must be a number more than 0", float)

        # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calc cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    # Find sub-total
    sub_total = expense_frame['Cost'].sum()

    # Currency formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


# Prints expense frames
def expense_print(heading, frame, subtotal):
    print(f"\n**** {heading} Costs ****")
    print(frame)
    print(f"\n{heading} Costs: ${subtotal:.2f}")
    return ""


# Gets profit goal
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


# **** Main routine goes here ****
# Get user data
product_name = not_blank("Product name: ", "The product name cannot be blank.")

print("\nPlease enter your variable costs below...")

# set variables
fixed_frame = ""
fixed_sub = 0
have_fixed = ""
variable_frame = ""
variable_sub = 0

# Get variable costs
while True:
    variable_expenses = get_expenses("variable")
    # if they haven't entered an item, return error
    if variable_expenses == "xxx":
        print("Please enter at least ONE item.")
        continue

    variable_frame = variable_expenses[0]
    variable_sub = variable_expenses[1]

    print()
    have_fixed = yes_no("Do you have fixed costs (y/n)?: ")

    if have_fixed == "yes":
        # Get fixed costs
        fixed_expenses = get_expenses("fixed")
        # break code even if they haven't entered an item
        if fixed_expenses == "xxx":
            have_fixed = "no"
            break

        fixed_frame = fixed_expenses[0]
        fixed_sub = fixed_expenses[1]
    else:
        fixed_sub = 0
        fixed_frame = ""


# Find total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculate recommended price
selling_price = 0

# Write data to file

# *** Printing area ***

print(f"\n**** Fund Raising - {product_name} *****")

expense_print("Variable", variable_frame, variable_sub)

if have_fixed == "yes":
    expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)

    print(f"\nTotal Expenses: ${all_costs}\n")

    print("\n**** Profit & Sales Targets ****")
    print(f"Profit Target: ${profit_target:.2f}")
    print(f"Total Sales: ${(all_costs + profit_target):.2f}")

    print(f"\n**** Recommended Selling Price: {selling_price:.2f}")
