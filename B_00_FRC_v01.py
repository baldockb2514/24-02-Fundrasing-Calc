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



