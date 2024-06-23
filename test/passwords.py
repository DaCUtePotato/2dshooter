import random
import string

def generate_random_string(length):
    # Define the possible characters: lowercase, uppercase, digits, and special characters
    all_characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a random string using the defined characters
    random_string = ''.join(random.choice(all_characters) for _ in range(length))

    return random_string

# Define the length of the random string
length_of_string = 10  # You can change this to any length you want

# Generate and print the random string
random_string = generate_random_string(length_of_string)
print("Random String:", random_string)
