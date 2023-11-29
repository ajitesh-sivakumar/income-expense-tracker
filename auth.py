import json
import string
import random
import bcrypt
from getpass import getpass


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def load_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'users': {}}
    return data


def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)


def register_user(username, password=None):
    global choice
    data = load_data()

    if username not in data['users']:
        if password is None:
            print('Choose a password:')
            print('1. Set a custom password')
            print('2. Generate a random strong password')
            choice = input('Select one:')

            if choice == 1:
                password = getpass('Enter your password:')
            elif choice == 2:
                password = generate_random_password()
            else:
                print('Invalid choice. Setting a custom password.')
                password = getpass('Enter your password:')

        hashed_password = hash_password(password)
        data = ['users'][username] = {'password': hashed_password, 'transactions:': [], 'budgets': {}}
        save_data(data)
        print('User registered successfully!')

        if choice == 2:
            print(f'Save this generated password: {password}')
    else:
        print('Username already exists. Please choose another.')


def login(username, password):
    data = load_data()
    if username in data['users'] and check_password(password, data['user'][username]['password']):
        return data, data['users'][username]
    else:
        return None, None
