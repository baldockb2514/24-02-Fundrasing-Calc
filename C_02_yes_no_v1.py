# Functions go here...

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



# Main routine goes here...
show_instructions = yes_no("Have you played this game before? ")

print("you chose {}".format(show_instructions))
print()
having_fun = yes_no("Are you having fun? ")
print("you said {} to having fun".format(having_fun))
