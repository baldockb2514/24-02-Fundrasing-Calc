# import libraries
import pandas
import math


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
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    return [expense_frame, sub_total]


# Prints expense frames
def expense_print(heading, frame, subtotal):
    return f"\n--- {heading} Costs ---\n{frame}\n| {heading} Costs Total: ${subtotal:.2f}"


# Gets profit goal
def profit_goal(total_costs):
    # Initialise variables and error message
    error = "Please enter a valid profit goal."

    while True:

        # Ask for profit goal...
        response = input("\nwhat is your profit goal? (eg $500 or 50%): ")

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
            dollar_type = yes_no(f"Did you mean ${amount:.2f}, ie {amount:.2f} dollars? y / n: ")

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no(f"Did you mean {amount}%, ie {amount} percent? y / n: ")

            # Set profit type based on user answer above
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return [amount, profit_type]
        else:
            goal = (amount / 100) * total_costs
            return [goal, profit_type]


# Rounding function
def round_up(amount, round_to):
    return int(math.ceil(amount / round_to)) * round_to


# Shows instructions
def show_instructions():
    print('''\n 
***** Instructions *****

This Program will ask you for...
- The name of the product that you are selling
- How many items you plan on selling
- The costs for each component of the product
- How much money you want to make

When you have entered all the items, press 'xxx' to quit.

The program will then display an itemised list of the costs
 with subtotals for the variable and fixed costs.
Finally it will tell you how much you should sell
 each item for to reach your profit goal.

The data will also be automatically written to a text file which
 has the same name as your product

**************************''')


# **** Main routine goes here ****
# Get user data

# ask user if they want to see the instructions
want_instructions = yes_no("Do you want to see the instructions for this program?: ")
if want_instructions == "yes":
    show_instructions()

product_name = not_blank("\nProduct name: ", "The product name cannot be blank.")
how_many = num_check("How many items will you be producing?: ", "The number of items should be a whole number more "
                                                                "than 0", int)

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

        break
    else:
        fixed_sub = 0
        fixed_frame = ""
        break

# Find total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calc total sales needed to reach goal
sales_needed = all_costs + profit_target[0]

# Ask user for rounding
to_round = num_check("Round to nearest...?: ", "Must be a whole number more than 0.", int)

# Calculate recommended price
selling_price = sales_needed / how_many
print(f"Selling Price (unrounded): ${selling_price:.2f}")

if profit_target[1] == "%":
    profit_target = round_up(sales_needed, to_round)
recommended_price = round_up(selling_price, to_round)

# Write data to file

# *** Printing area ***

print(f"\n**** Fund Raising - {product_name} *****")

total_expenses = f"Total Expenses: ${all_costs:.2f}"

profit_target = f"**** Profit & Sales Targets ****\nProfit Target: ${profit_target[1]:.2f}"

pricing = f"**** Pricing ****\nMinimum Price: ${selling_price:.2f}\n" \
          f"Recommended Price: ${recommended_price:.2f}"

# Write to file...

# Create file to hold data (add .txt extension)
file_name = f"{product_name}.txt"
text_file = open(file_name, "w+")

# Change frames to strings
variable_txt = expense_print("Variable", variable_frame, variable_sub)


if have_fixed == "no":
    fixed_txt = ""
else:
    fixed_txt = expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)

to_write = [variable_txt, fixed_txt, total_expenses,
            profit_target, pricing]

# heading
for item in to_write:
    item = str(item)
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()

# Print stuff
for item in to_write:
    print(item)
    print()
