
def menu():
    menu = """\n
    --------------- MENU ----------------
    [d]\tdeposit
    [w]\twithdraw
    [b]\tbank_statement
    [na]\tNew account
    [sa]\tShow accounts
    [nu]\tNew user
    [q]\tQuit
    => """
    return input(menu)

def deposit(account_balance, amount, bank_statement, /):
    if amount > 0:
        account_balance += amount
        bank_statement += f"Deposit:\tR$ {amount:.2f}\n"
        print("\n-- Deposit Successful --")
    else:
        print("\nXX Invalid amount XX")

    return account_balance, bank_statement

def withdraw(*, account_balance, amount, bank_statement, limit, number_of_withdraws, withdraw_limit):
    exceeded_account_balance = amount > account_balance
    exceeded_limit = amount > limit
    exceeded_withdraws = number_of_withdraws >= withdraw_limit

    if exceeded_account_balance:
        print("\nXX Insufficient account balance XX")

    elif exceeded_limit:
        print("\nXX Withdraw amount exceeded limit XX")

    elif exceeded_withdraws:
        print("\nXX number of withdraws exceeded XX")

    elif amount > 0:
        account_balance -= amount
        bank_statement += f"withdraw:\t\tR$ {amount:.2f}\n"
        number_of_withdraws += 1
        print("\n-- withdraw successful --")

    else:
        print("\nXX Invalid amount XX")

    return account_balance, bank_statement

def show_bank_statement(account_balance, /, *, bank_statement):
    print("\n----------- bank_statement -----------")
    if bank_statement:  
        print(bank_statement)
    print(f"\naccount_balance:\t\tR$ {account_balance:.2f}")
    print("----------------------------------------")

def new_user(users):
    cpf = input("CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\nXX Invalid CPF XX")
        return

    name = input("Name: ")
    date_of_birth = input("Date of Birth: ")
    address = input("Address: ")

    users.append({"name": name, "date_of_birth": date_of_birth, "cpf": cpf, "address": address})

    print("-- New user added --")

def filter_user(cpf, users):
    users_filtered = [user for user in users if user["cpf"] == cpf]
    return users_filtered[0] if users_filtered else None

def new_account(branch, account_number, users):
    cpf = input("CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\n-- New account created --")
        return {"branch": branch, "account_number": account_number, "user": user}

    print("\nXX Invalid User XX")

def display_accounts(accounts):
    for account in accounts:
        display = f"""\
            Branch:\t{account['branch']}
            C/C:\t\t{account['account_number']}
            Account holder:\t{account['user']['name']}
        """
        print("=" * 100)
        print(display)

def main():
    withdraw_limit = 3
    branch = "0001"

    account_balance = 0
    limit = 500
    bank_statement = ""
    number_of_withdraws = 0
    users = []
    accounts = []

    while True:
        selected_menu = menu()

        if selected_menu == "d":
            amount = float(input("Deposit amount: "))

            account_balance, bank_statement = deposit(account_balance, amount, bank_statement)

        elif selected_menu == "w":
            amount = float(input("Withdraw amount: "))

            account_balance, bank_statement = withdraw(
                account_balance=account_balance,
                amount=amount,
                bank_statement=bank_statement,
                limit=limit,
                number_of_withdraws=number_of_withdraws,
                withdraw_limit=withdraw_limit,
            )

        elif selected_menu == "b":
            show_bank_statement(account_balance, bank_statement=bank_statement)

        elif selected_menu == "nu":
            new_user(users)

        elif selected_menu == "na":
            account_number = len(accounts) + 1
            account = new_account(branch, account_number, users)

            if account:
                accounts.append(account)

        elif selected_menu == "sa":
            display_accounts(accounts)

        elif selected_menu == "q":
            break

        else:
            print("Invalid input")

main()
