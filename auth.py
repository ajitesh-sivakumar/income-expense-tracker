import json
import string
import random
import bcrypt
import base64

from getpass import getpass


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def hash_data(data):
    salt = bcrypt.gensalt()
    hashed_data = bcrypt.hashpw(data.encode('utf-8'), salt)
    return base64.b64encode(hashed_data).decode('utf-8')


def check_hashed_data(plain_data, hashed_data):
    hashed_data_bytes = base64.b64decode(hashed_data.encode('utf-8'))
    return bcrypt.checkpw(plain_data.encode('utf-8'), hashed_data_bytes)


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


def register(username):
    data = load_data()
    password = None

    if username not in data['users']:
        if password is None:
            print('Choose a password:')
            print('1. Set a custom password')
            print('2. Generate a random strong password')

            choice = input('Select one:')

            try:
                choice = int(choice)
            except ValueError:
                print('Invalid choice. Setting a custom password.')
                choice = 1

            if choice == 1:
                password = getpass('Enter your password:')
            elif choice == 2:
                password = generate_random_password()
                print(f'Save this generated password: {password}')
            else:
                print('Invalid choice. Setting a custom password.')
                password = getpass('Enter your password:')

        security_question = input('Enter your security question:')
        security_answer = getpass('Enter the answer to your security question:')
        hashed_security_answer = hash_data(security_answer)

        hashed_password = hash_data(password)
        data['users'][username] = {
            'password': hashed_password,
            'security_question': security_question,
            'security_answer': hashed_security_answer,
            'transactions': [],
        }
        save_data(data)
        print('User registered successfully!')
    else:
        print('Username already exists. Please choose another.')


def login(username, password):
    data = load_data()
    if username in data['users'] and check_hashed_data(password, data['users'][username]['password']):
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
