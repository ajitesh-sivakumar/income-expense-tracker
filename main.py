from getpass import getpass

from auth import register, login, forgot_password
from transactions import add_transaction, view_transaction, edit_transaction, delete_transaction, view_all_transactions


def display_login_menu():
    print("1. Login")
    print("2. Register")
    print("3. Forgot Password")
    print("4. Exit")


def display_main_menu(username):
    print(f"Welcome, {username}!")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Edit Transaction")
    print("4. Delete Transaction")
    print("5. View All Transactions")
    print("6. Logout")
    print("7. Exit")


def main():
    logged_in_user = None
    while True:
        if logged_in_user is None:
            display_login_menu()
        else:
            display_main_menu(logged_in_user)

        choice = input("Enter your choice: ")

        if logged_in_user is None:
            if choice == '1':
                username = input("Enter your username: ")
                password = getpass("Enter your password: ")
                data, user = login(username, password)
                if user:
                    logged_in_user = username
                    print(f"Logged in as {username}")
                else:
                    print("Invalid username or password.")
            elif choice == '2':
                username = input("Enter your username: ")
                register(username)
            elif choice == '3':
                username = input("Enter your username: ")
                forgot_password(username)
            elif choice == '4':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
        else:
            if choice == '1':
                add_transaction(logged_in_user)
            elif choice == '2':
                view_transaction(logged_in_user)
            elif choice == '3':
                edit_transaction(logged_in_user)
            elif choice == '4':
                delete_transaction(logged_in_user)
            elif choice == '5':
                view_all_transactions()
            elif choice == '6':
                logged_in_user = None
                print("Logged out successfully.")
            elif choice == '7':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
