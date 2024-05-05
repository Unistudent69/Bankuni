from abc import ABC, abstractmethod

class BalanceException(Exception):
    pass

class Account(ABC):
    MIN_BALANCE = 50  # Osztályszintű konstans
    
    def __init__(self, initialAmount, accName):
        self.balance = initialAmount
        self.name = accName
        print(f"\nAccount '{self.name}' created.\nBalance = ${self.balance:.2f}")
    
    @abstractmethod
    def deposit(self, amount):
        pass

    def viableTransaction(self, amount):
        if self.balance >= amount:
            return
        else:
            raise BalanceException(
                f"\nSorry, account '{self.name}' only has a balance of ${self.balance:.2f}")

    def getBalance(self):
        print(f"\nAccount '{self.name}' balance = $ {self.balance:.2f}")

class BankAccount(Account):
    def __init__(self, initialAmount, accName, other_accounts=None):
        super().__init__(initialAmount, accName)
        if other_accounts is None:
            other_accounts = []
        self.other_accounts = other_accounts  # Aggregáció

    def deposit(self, amount):
        self.balance = self.balance + amount
        print("\nDeposit complete.")
        self.getBalance()
        
    def withdraw(self, amount):
        try:
            self.viableTransaction(amount)
            self.balance = self.balance - amount
            print("\nWithdraw complete.")
            self.getBalance()
        except BalanceException as error:
            print(f'\nWithdraw interrupted: {error}')

    def transfer(self, amount, account):
        try:
            print('\n**********\n\nBeginning transfer..💵')
            self.viableTransaction(amount)
            self.withdraw(amount)
            account.deposit(amount)
            print('\nTransfer complete! ✅\n\n**********')
        except BalanceException as error:
            print(f'\nTransfer interrupted. ❌ {error}')

class InterestRewardAcct(BankAccount):
    INTEREST_RATE = 1.05  # Osztályszintű konstans

    def deposit(self, amount):
        super().deposit(amount * self.INTEREST_RATE)

class SavingsAccount(InterestRewardAcct):
    def __init__(self, initialAmount, accName, transaction_fee=5):
        super().__init__(initialAmount, accName)
        self.fee = transaction_fee

    def withdraw(self, amount):
        try:
            self.viableTransaction(amount + self.fee)
            self.balance = self.balance - (amount + self.fee)
            print("\nWithdraw complete.")
            self.getBalance()
        except BalanceException as error:
            print(f'\nWithdraw interrupted: {error}')    

def main():
    # Létrehozás és műveletek
    savings = SavingsAccount(1000, "Savings")
    checking = BankAccount(500, "Checking", [savings])
    accounts = [savings, checking]

    # Demonstráció: Befizetés, kivétel és átutalás
    checking.deposit(200)
    savings.withdraw(100)
    checking.transfer(150, savings)

if __name__ == "__main__":
    main()
