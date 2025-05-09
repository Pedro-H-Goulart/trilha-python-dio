def display_menu():
    menu = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [b]\tBank Statement
    [na]\tNew Account
    [sa]\tShow Accounts
    [nu]\tNew User
    [q]\tQuit
    => """
    return input(menu.strip())

def deposit(balance, amount, statement):
    if amount > 0:
        balance += amount
        statement += f"Deposit:\tR$ {amount:.2f}\n"
        print("\n-- Deposit Successful --")
    else:
        print("\n!! Invalid Amount !!")

    return balance, statement

def withdraw(*, balance, amount, statement, limit, withdrawals_count, withdrawal_limit):
    exceeded_balance = amount > balance
    exceeded_limit = amount > limit
    exceeded_withdrawals = withdrawals_count >= withdrawal_limit

    if exceeded_balance:
        print("\n!! Insufficient Funds !!")
    elif exceeded_limit:
        print("\n!! Exceeded Withdrawal Limit !!")
    elif exceeded_withdrawals:
        print("\n!! Maximum Withdrawals Reached !!")
    elif amount > 0:
        balance -= amount
        statement += f"Withdrawal:\tR$ {amount:.2f}\n"
        withdrawals_count += 1
        print("\n-- Withdrawal Successful --")
    else:
        print("\n!! Invalid Amount !!")

    return balance, statement, withdrawals_count

def show_statement(balance, /, *, statement):
    header = "=============== BANK STATEMENT ==============="
    print(f"\n{header}")
    if statement:
        print(statement)
    print(f"\nCurrent Balance:\tR$ {balance:.2f}")
    print("=" * len(header))

def create_user(users):
    cpf = input("CPF (numbers only): ").strip()
    if any(user["cpf"] == cpf for user in users):
        print("\n!! CPF Already Registered !!")
        return

    user_data = {
        "name": input("Full Name: ").title(),
        "dob": input("Date of Birth (DD/MM/YYYY): ").strip(),
        "cpf": cpf,
        "address": input("Address (Street, No - City/ST): ").strip()
    }
    
    users.append(user_data)
    print("\n-- User Created Successfully --")

def find_user(cpf, users):
    return next((user for user in users if user["cpf"] == cpf), None)

def create_account(branch, account_number, users):
    cpf = input("User CPF: ").strip()
    user = find_user(cpf, users)
    
    if not user:
        print("\n!! User Not Found !!")
        return None
    
    account = {
        "branch": branch,
        "number": account_number,
        "user": user
    }
    print("\n-- Account Created Successfully --")
    return account

def show_accounts(accounts):
    if not accounts:
        print("\n-- No Accounts Registered --")
        return
    
    for account in accounts:
        line = "=" * 50
        details = (
            f"Branch:\t\t{account['branch']}\n"
            f"Account:\t{account['number']}\n"
            f"Holder:\t\t{account['user']['name']}"
        )
        print(f"\n{line}\n{details}\n{line}")

def main():
    WITHDRAWAL_LIMIT = 3
    DAILY_LIMIT = 500
    BRANCH_CODE = "0001"

    balance = 0
    statement = ""
    withdrawals_count = 0
    users = []
    accounts = []

    while True:
        option = display_menu().lower()

        if option == "d":
            amount = float(input("Deposit Amount: R$ "))
            balance, statement = deposit(balance, amount, statement)

        elif option == "w":
            amount = float(input("Withdrawal Amount: R$ "))
            result = withdraw(
                balance=balance,
                amount=amount,
                statement=statement,
                limit=DAILY_LIMIT,
                withdrawals_count=withdrawals_count,
                withdrawal_limit=WITHDRAWAL_LIMIT
            )
            balance, statement, withdrawals_count = result

        elif option == "b":
            show_statement(balance, statement=statement)

        elif option == "nu":
            create_user(users)

        elif option == "na":
            new_account = create_account(BRANCH_CODE, len(accounts) + 1, users)
            if new_account:
                accounts.append(new_account)

        elif option == "sa":
            show_accounts(accounts)

        elif option == "q":
            print("\n-- System Closed --")
            break

        else:
            print("\n!! Invalid Option !!")

if __name__ == "__main__":
    main()