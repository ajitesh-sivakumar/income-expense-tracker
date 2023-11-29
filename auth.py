import json
import string
import random
import bcrypt
from getpass import getpass


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def hash_data(data):
    salt = bcrypt.gensalt()
    hashed_data = bcrypt.hashpw(data.encode('utf-8'), salt)
    return hashed_data


def check_hashed_data(plain_data, hashed_data):
    return bcrypt.checkpw(plain_data.encode('utf-8'), hashed_data)


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

        security_question = input('Enter your security question:')
        security_answer = getpass('Enter the answer to your security question:')
        hashed_security_answer = hash_data(security_answer)

        hashed_password = hash_data(password)
        data = ['users'][username] = {
            'password': hashed_password,
            'security_question': security_question,
            'security_answer': hashed_security_answer,
            'transactions:': [],
            'budgets': {}}
        save_data(data)
        print('User registered successfully!')

        if choice == 2:
            print(f'Save this generated password: {password}')
    else:
        print('Username already exists. Please choose another.')


def login(username, password):
    data = load_data()
    if username in data['users'] and check_hashed_data(password, data['user'][username]['password']):
        return data, data['users'][username]
    else:
        return None, None


def forgot_password(username):
    data = load_data()
    if username in data['users']:
        user = data['users'][username]
        print(f"Security Question: {user['security_question']}")
        answer_attempt = getpass('Enter the answer:')
        if check_hashed_data(answer_attempt, user['security_answer']):
            new_password = getpass('Enter new password:')
            hashed_new_password = hash_data(new_password)
            user['password'] = hashed_new_password
            save_data(data)
            print('Password changed successfully.')
        else:
            print('Incorrect answer! Password reset failed.')
    else:
        print('User not found!')
