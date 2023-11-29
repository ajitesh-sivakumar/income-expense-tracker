import json

def load_data():
    # Load data from the 'data.json' file or initialize an empty dictionary if the file doesn't exist.
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'users': {}}
    return data

def save_data(data):
    # Save the data dictionary to the 'data.json' file.
    with open('data.json', 'w') as file:
        json.dump(data, file)

def get_user_data(username):
    # Retrieve user data (if exists) from the loaded data dictionary.
    data = load_data()
    return data['users'].get(username, {})

def update_user_data(username, key, value):
    # Update a specific key in the user's data dictionary and save the changes.
    data = load_data()
    data['users'][username][key] = value
    save_data(data)

def create_transaction(username, amount, category):
    # Add a new transaction to the user's transactions list and update the user's data.
    user_data = get_user_data(username)
    transactions = user_data.get('transactions', [])
    transactions.append({'amount': amount, 'category': category})
    update_user_data(username, 'transactions', transactions)
    print("Transaction added successfully.")

def read_transactions(username):
    # Display all transactions for a specific user.
    user_data = get_user_data(username)
    transactions = user_data.get('transactions', [])
    if transactions:
        print(f"Transactions for {username}:")
        for transaction in transactions:
            print(f"Amount: {transaction['amount']}, Category: {transaction['category']}")
    else:
        print(f"No transactions for {username}.")

def update_transaction(username, index, amount, category):
    # Update a transaction at a specific index for a given user.
    user_data = get_user_data(username)
    transactions = user_data.get('transactions', [])
    if transactions:
        if 0 <= index < len(transactions):
            transactions[index] = {'amount': amount, 'category': category}
            update_user_data(username, 'transactions', transactions)
            print("Transaction updated successfully.")
        else:
            print("Invalid index.")
    else:
        print(f"No transactions for {username}.")

def delete_transaction(username, index):
    # Delete a transaction at a specific index for a given user.
    user_data = get_user_data(username)
    transactions = user_data.get('transactions', [])
    if transactions:
        if 0 <= index < len(transactions):
            del transactions[index]
            update_user_data(username, 'transactions', transactions)
            print("Transaction deleted successfully.")
        else:
            print("Invalid index.")
    else:
        print(f"No transactions for {username}.")

def view_all_transactions():
    # Display all transactions for all users.
    data = load_data()

    print("All Transactions:")
    for username, user_data in data['users'].items():
        transactions = user_data.get('transactions', [])
        if transactions:
            print(f"Transactions for {username}:")
            for transaction in transactions:
                print(f"Amount: {transaction['amount']}, Category: {transaction['category']}")
        else:
            print(f"No transactions for {username}.")

if __name__ == "__main__":
    # You can add test cases or use this block for running the module independently.
    pass
