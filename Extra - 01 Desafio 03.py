from abc import ABC, abstractmethod
from datetime import datetime

class Customer:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)

class Individual(Customer):
    def __init__(self, name, birth_date, ssn, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.ssn = ssn

class Account:
    def __init__(self, number, customer):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._customer = customer
        self._history = History()

    @classmethod
    def new_account(cls, customer, number):
        return cls(number, customer)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def customer(self):
        return self._customer

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        balance = self.balance
        insufficient_balance = amount > balance

        if insufficient_balance:
            print("\n!!! Operation failed! Insufficient balance. !!!")
        elif amount > 0:
            self._balance -= amount
            print("\n=== Withdrawal successful! ===")
            return True
        else:
            print("\n!!! Operation failed! Invalid amount. !!!")
        return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Deposit successful! ===")
            return True
        else:
            print("\n!!! Operation failed! Invalid amount. !!!")
            return False

class CheckingAccount(Account):
    def __init__(self, number, customer, limit=500, withdrawal_limit=3):
        super().__init__(number, customer)
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        withdrawal_count = len(
            [t for t in self.history.transactions if t["type"] == Withdrawal.__name__]
        )

        exceeds_limit = amount > self.limit
        exceeds_withdrawals = withdrawal_count >= self.withdrawal_limit

        if exceeds_limit:
            print("\n!!! Operation failed! Withdrawal amount exceeds limit. !!!")
        elif exceeds_withdrawals:
            print("\n!!! Operation failed! Maximum withdrawals exceeded. !!!")
        else:
            return super().withdraw(amount)
        return False

    def __str__(self):
        return f"""
            Agency:\t{self.agency}
            A/C:\t\t{self.number}
            Owner:\t{self.customer.name}
        """

class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append({
            "type": transaction.__class__.__name__,
            "amount": transaction.amount,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })

class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @abstractmethod
    def register(self, account):
        pass

class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        if account.withdraw(self.amount):
            account.history.add_transaction(self)

class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        if account.deposit(self.amount):
            account.history.add_transaction(self)

class BankingSystem:
    def __init__(self):
        self.customers = []
        self.accounts = []
        self.account_counter = 1

    def find_customer(self, ssn):
        for customer in self.customers:
            if isinstance(customer, Individual) and customer.ssn == ssn:
                return customer
        return None

    def find_account(self, account_number):
        for account in self.accounts:
            if account.number == account_number:
                return account
        return None

    def create_customer(self):
        print("\n=== Create New Customer ===")
        name = input("Full name: ")
        birth_date = input("Birth date (DD-MM-YYYY): ")
        ssn = input("SSN: ")
        address = input("Address: ")
        
        if self.find_customer(ssn):
            print("\n!!! Customer with this SSN already exists !!!")
            return
        
        customer = Individual(name, birth_date, ssn, address)
        self.customers.append(customer)
        print("\n=== Customer created successfully! ===")

    def create_account(self):
        print("\n=== Create New Account ===")
        ssn = input("Customer SSN: ")
        customer = self.find_customer(ssn)
        
        if not customer:
            print("\n!!! Customer not found !!!")
            return
        
        account = CheckingAccount(self.account_counter, customer)
        self.accounts.append(account)
        customer.add_account(account)
        self.account_counter += 1
        print("\n=== Account created successfully! ===")
        print(account)

    def deposit(self):
        print("\n=== Deposit ===")
        account_number = int(input("Account number: "))
        account = self.find_account(account_number)
        
        if not account:
            print("\n!!! Account not found !!!")
            return
        
        amount = float(input("Amount to deposit: "))
        transaction = Deposit(amount)
        transaction.register(account)

    def withdraw(self):
        print("\n=== Withdraw ===")
        account_number = int(input("Account number: "))
        account = self.find_account(account_number)
        
        if not account:
            print("\n!!! Account not found !!!")
            return
        
        amount = float(input("Amount to withdraw: "))
        transaction = Withdrawal(amount)
        transaction.register(account)

    def show_statement(self):
        print("\n=== Bank Statement ===")
        account_number = int(input("Account number: "))
        account = self.find_account(account_number)
        
        if not account:
            print("\n!!! Account not found !!!")
            return
        
        print(f"\nAgency: {account.agency}")
        print(f"Account: {account.number}")
        print(f"Owner: {account.customer.name}")
        print("\nTransactions:")
        
        for transaction in account.history.transactions:
            print(f"{transaction['date']} - {transaction['type']}: ${transaction['amount']:.2f}")
        
        print(f"\nCurrent Balance: ${account.balance:.2f}")

    def list_accounts(self):
        print("\n=== All Accounts ===")
        for account in self.accounts:
            print(account)
            print("Balance:", account.balance)
            print("--------------------")

    def menu(self):
        while True:
            print("\n===== Banking System =====")
            print("1. Create Customer")
            print("2. Create Account")
            print("3. Deposit")
            print("4. Withdraw")
            print("5. Bank Statement")
            print("6. List All Accounts")
            print("0. Exit")
            
            choice = input("Select an option: ")
            
            if choice == "1":
                self.create_customer()
            elif choice == "2":
                self.create_account()
            elif choice == "3":
                self.deposit()
            elif choice == "4":
                self.withdraw()
            elif choice == "5":
                self.show_statement()
            elif choice == "6":
                self.list_accounts()
            elif choice == "0":
                print("\n=== Exiting system ===")
                break
            else:
                print("\n!!! Invalid option !!!")

if __name__ == "__main__":
    bank = BankingSystem()
    bank.menu()