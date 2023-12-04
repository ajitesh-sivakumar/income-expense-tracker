import json


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


def get_user_transactions(username):
    data = load_data()
    return data['users'].get(username, {}).get('transactions', [])


def update_user_transactions(username, transactions):
    data = load_data()
    data['users'][username]['transactions'] = transactions
    save_data(data)


def add_transaction(username):
    amount = float(input("Enter the transaction amount: "))
    description = input("Enter the transaction description: ")

    transactions = get_user_transactions(username)
    transactions.append({'amount': amount, 'description': description})

    update_user_transactions(username, transactions)
    print("Transaction added successfully.")


def view_transaction(username, index=None):
    transactions = get_user_transactions(username)

    if transactions:
        if index is None:
            index = int(input("Enter the index of the transaction to view: "))
        if 0 <= index < len(transactions):
            print(f"Transaction details for {username}, index {index}:")
            transaction = transactions[index]
            print(f"Amount: {transaction['amount']}, Description: {transaction['description']}")
        else:
            print("Invalid index.")
    else:
        print(f"No transactions for {username}.")


def edit_transaction(username):
    transactions = get_user_transactions(username)
    if transactions:
        index = int(input("Enter the index of the transaction to edit: "))
        view_transaction(username)  # Prompt for the index and show the details
        if 0 <= index < len(transactions):
            amount = float(input("Enter the new transaction amount: "))
            description = input("Enter the new transaction description: ")
            transactions[index] = {'amount': amount, 'description': description}
            update_user_transactions(username, transactions)
            print("Transaction edited successfully.")
        else:
            print("Invalid index.")
    else:
        print(f"No transactions for {username}.")


def delete_transaction(username):
    transactions = get_user_transactions(username)
    if transactions:
        index = int(input("Enter the index of the transaction to delete: "))
        view_transaction(username, index)
        if 0 <= index < len(transactions):
            del transactions[index]
            update_user_transactions(username, transactions)
            print("Transaction deleted successfully.")
        else:
            print("Invalid index.")
    else:
        print(f"No transactions for {username}.")


def view_all_transactions():
    data = load_data()

    print("All Transactions:")
    for username, user_data in data['users'].items():
        transactions = user_data.get('transactions', [])
        if transactions:
            print(f"Transactions for {username}:")
            for transaction in transactions:
                print(f"Amount: {transaction['amount']}, Description: {transaction['description']}")
        else:
            print(f"No transactions for {username}.")

# Example usage:
# Uncomment the next lines for testing
# username = 'example_user'
# add_transaction(username)
# add_transaction(username)
# view_transaction(username)
# edit_transaction(username)
# view_all_transactions()
