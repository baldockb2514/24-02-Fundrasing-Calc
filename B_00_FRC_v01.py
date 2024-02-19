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
