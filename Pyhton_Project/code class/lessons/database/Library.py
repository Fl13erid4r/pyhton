import datbase2

def user(username):
    while True:
        print("\nLibrary Menu:")
        print("1. View Available Books")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. View loans")
        print("5. Donate a Book")
        print("6. View Book Details")
        print("7. View My Detail")
        print("8. Change My Detail")
        print("9. Exit")

        choice = input("Enter your choice: ")
        if not choice.isdigit():
            print("Please enter a valid number")
            continue
        choice = int(choice)

        if choice == 1:
            datbase2.available_books()
        elif choice == 2:
            datbase2.borrow_book(username)
        elif choice == 3:
            datbase2.return_book(username)
        elif choice == 4:
            datbase2.view_loans(username)
        elif choice == 5:
            datbase2.donate_book()
        elif choice == 6:
            datbase2.book_info()
        elif choice == 7:
            datbase2.user_info(username)
        elif choice == 8:
            datbase2.change_details(username)
        elif choice == 9:
            print("Logging out...")
            break
        else:
            print("Invalid choice")

def admin():
    while True:
        print("\nAdmin Menu:\n")
        print("1. Add a new book")
        print("2. Update a book")
        print("3. Delete a book")
        print("4. View all books")
        print("5. Exit\n")

        choice = input("Enter your choice: ")
        if not choice.isdigit():
            print("Please enter a valid number")
            continue
        choice = int(choice)

        if choice == 1:
            datbase2.add_new_book()
        elif choice == 2:
            datbase2.update_book()
        elif choice == 3:
            datbase2.delete_book()
        elif choice == 4:
            datbase2.available_books()
        elif choice == 5:
            print("Logging out...")
            break
        else:
            print("Invalid choice")

def run():
    username = None
    while not username:
        username = datbase2.enter()
        if username is None:
            print("Login or signup failed, please try again.")

    if username.lower() == "admin":
        admin()
    else:
        user(username)
    print("Thank you for using the Library")
    datbase2.close_db()

if __name__ == "__main__":
    print("Welcome to the Library")
    run()

