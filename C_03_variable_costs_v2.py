import pandas


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


# Gets expenses, returns list which has the dat frame and sub total
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
            break

        print()

        quantity = num_check("Quantity: ", "The amount must be a whole number more than 0", int)

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


# *** Printing area ***

# Get user data
product_name = not_blank("Product name: ", "The product name cannot be blank.")

variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

print()
print(variable_frame)
print()

print(f"Variable Costs: ${variable_sub:.2f}")
