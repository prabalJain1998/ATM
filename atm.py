import csv
import pandas as pd  # imported pandas
from datetime import date  # imported date
from datetime import datetime as dt
import warnings  # warnings package

warnings.filterwarnings("ignore")  # ignoring the warnings

#class for authenticating the user
class Authentication():

    def __init__(self):
        pass

    def check(self, username, password):
        auth = pd.read_csv('auth.csv')  # reading the csv file(already present as a database)
        login = auth[auth['Account'] == username]
        # print((login['Password'] == password).bool())
        if ((login['Password'] == int(password)).bool()):  # checking if the PIN in csv file matches the entered PIN by the user
            print('*' * 25)
            print('     Welcome {}'.format(username))  # if PIN is correct, a welcome message is printed on console
            print('*' * 25)
            return True  # return true if authenticated
        else:
            # print('Please input a valid 4-digit PIN')
            return False  # if password doesnot match ,return false


#class for changing PIN
class ChangePin():
    def __init__(self):
        pass

    def change_pin(self, pin, u):
        self.u = u
        df = pd.DataFrame(pd.read_csv('auth.csv'))  # reading the "auth.csv" file to get credentials
        for i in range(len(df)):
            if (df['Account'][i] == u.username):
                # print(df['Account'][i])
                df.at[i, 'Password'] = pin
        print('Pin Change Successful')
        df.to_csv('auth.csv', index=False)  # after changing the PIN, reflect the changes in the csv file


# class for Balance
class Balance():
    def __init__(self):
        pass

    def balance(self, act, u):
        self.u = u
        user = u.username + '.csv'
        df = pd.DataFrame(pd.read_csv(user))  # read the csv file of the user, who is currently logged in
        i = df[df['Type'] == act].index.tolist()  # check if the 'Type' of account matches as entered by the user i.e 'Savings' or 'Current'
        # print(df['Amount'].values[i][len(i) - 1])
        # return the last updated amount of 'Type' = act
        return df['Amount'].values[i][len(i) - 1]


# class for amount withdrawal
class Withdrawal():
    def __init__(self):
        pass

    def withdraw(self, amount, date, act, u):
        user = u.username + '.csv'
        df = pd.DataFrame(pd.read_csv(user))  # read the csv file of the user, who is currently logged in
        balance = u.balance(act, u)  # get current (last updated) balance from the balance function
        # check if the amount to be withdrawn is less than the current balance, also greater than the minimum balance i.e Rs. 1000
        if (balance >= amount and (balance - amount >= 1000)):
            df2 = {'Date': date.strftime('%d-%m-%Y'), 'Debit': amount, 'Credit': 0, 'Amount': balance - amount,'Type': act}  # update the data after withdrawal
            df = df.append(df2, ignore_index=True)  # append the value to the dataframe in csv file
            print('Withdrawal Successfull')
            print('Your current balance is : ', balance - amount)  # display current balance after withdrawal
            df.to_csv(user, index=False)  # reflect the changes made in the csv file
        else:
            print('Enter a valid amount')


# class for amount deposit
class Deposit():
    def __init__(self):
        pass

    def deposit(self, amount, date, act, u):
        user = u.username + '.csv'
        df = pd.DataFrame(pd.read_csv(user))  # read the csv file of the user, who is currently logged in
        balance = u.balance(act, u)  # get current (last updated) balance from the balance function
        if (amount <= 25000):  # checking max credit limit
            df2 = {'Date': date.strftime('%d-%m-%Y'), 'Debit': 0, 'Credit': amount, 'Amount': balance + amount,'Type': act}  # update the data after deposit
            df = df.append(df2, ignore_index=True)  # append the value to the dataframe in csv file
            print('Deposit Successfull')
            print('Your current balance is : ', balance + amount)  # display current balance after deposit
            df.to_csv(user, index=False)  # reflect the changes made in the csv file
        else:
            print("Credit limit exceeded !")


# class for transaction summary between given start date and end date
class TransactionSummary():
    def __init__(self):
        pass

    def transaction_summary(self, act, start_date, end_date, u):
        user = u.username + '.csv'
        df = pd.DataFrame(pd.read_csv(user))  # read the csv file of the user, who is currently logged in
        df = df[df['Type'] == act]  # checking for the 'Type' of account i.e Savings or Current
        for row in df.values:
            date = row[0]  # date values
            d = dt.strptime(date, '%d-%m-%Y')  # getting date in correct format
            s = dt.strptime(start_date, '%d-%m-%Y')
            e = dt.strptime(end_date, '%d-%m-%Y')
            if (d >= s and d <= e):  # checking the transaction between start and the end date
                print("Date : {}, Debit : {}, Credit : {}, Amount : {}".format(row[0], row[1], row[2], row[3]))  # printing the transactions


#class user for various users
class User(Authentication, ChangePin, Balance, Withdrawal, Deposit, TransactionSummary):
    def __init__(self, username, password):
        self.username = username
        self.password = password


print('*'*25)
print(' THE ATM SYSTEM MACHINE')
print('*'*25)
print('Enter your Card:') #enter your card no.
username = input()
print('Enter your 4 digit PIN:') #enter your PIN
password = int(input())

#calling the object of class User, by passing username and password
user_1 = User(username, password)


# only authenticated user will be able to log in and will see the options
if (user_1.check(username, password)):
    while(1):
        print('*'*25)
        #Enter the mentioned digits to choose an option
        print('Enter 1 for PIN Change')
        print('Enter 2 for Balance Enquiry')
        print('Enter 3 For Amount Withdrawal')
        print('Enter 4 for Amount Deposit')
        print('Enter 5 for Transaction Summary')
        print('Enter 0 to quit')
        print('*' * 25)

        # take input
        inp = int(input())

        # input = 1 for changing the PIN
        if (inp == 1):
            print('Enter "N" for new PIN:')
            print('Enter "Q" to exit')
            act = input()
            if (act == 'N'):
                print('Enter new PIN')
                pin = input()
                if (len(pin) != 4):  # if entered pin is other than a four digit number, then print invalid PIN
                    print('Enter a valid 4-digit PIN!')
                else:
                    user_1.change_pin(pin, user_1) # else call change_pin to change the PIN
            elif (act == 'Q'):
                print("Thankyou for using the service.")
            else:
                print('Please enter a valid input')

        # input = 2 for balance enquiry
        elif (inp == 2):
            print('Enter "S" for Savings Account Balance Enquiry')
            print('Enter "C" for Current Account Balance Enquiry')
            print('Enter "Q" to exit')
            act = input()
            if (act == 'S'):
                print(user_1.balance(act, user_1))  # print balance of Savings Type
            elif (act == 'C'):
                print(user_1.balance(act, user_1))  # print balance of Current Type
            elif (act == 'Q'):
                print('Thankyou for using the service.')
            else:
                print('PLease enter a valid input')

        # input = 3 for amount withdrawal
        elif (inp == 3):
            print('Enter "S" for Savings Account Withdrawal:')
            print('Enter "C" for Current Account Withdrawal:')
            print('Enter "Q" to exit')
            act = input()
            if (act == 'S' or act == 'C'):
                print('Enter amount you want to Withdraw:')
                amount = input()
                if (amount != 'Q'):
                    # get today's date i.e date of transaction
                    user_1.withdraw(int(amount), date.today(), act, user_1) # calling withdrawal method
                elif (amount == 'Q'):  # exit
                    print('Thankyou for using the service.')
            elif (act == 'Q'):
                print('Thankyou for using the service.')
            else:
                print('Please enter a valid input')

        # input = 4 for amount deposit
        elif (inp == 4):
            print('Enter "S" for Savings Account Deposit')
            print('Enter "C" for Current Account Deposit')
            print('Enter "Q" to exit')
            act = input()
            if (act == 'S' or act == 'C'):
                print('Enter amount you want to Deposit:')
                print('Enter "Q" to exit')
                amount = input()
                if (amount != 'Q'):
                    # get today's date i.e date of transaction
                    user_1.deposit(int(amount), date.today(), act, user_1)  # calling deposit method
                elif (amount == 'Q'):
                    print('Thankyou for using the service.')
            elif (act == 'Q'):
                print('Thankyou for using the service.')
            else:
                print('Please enter a valid input')

        # input = 5 for transaction summary
        elif (inp == 5):
            print('Enter "S" for Savings Account Transaction Summary')
            print('Enter "C" for Current Account Transaction Summary')
            print('Enter "Q" to exit')
            act = input()
            if (act == 'S' or act == 'C'):
                print('Enter Start date in the format dd-mm-yyyy')
                start_date = input()
                print('Enter end date in the format dd-mm-yyyy')
                end_date = input()
                user_1.transaction_summary(act, start_date, end_date, user_1)  # calling Transaction_summary for listing the transactions
            elif (act == 'Q'):
                print('Thankyou for using the service.')
            else:
                print('Please enter a valid input')

        # enter 0 to exit and logging out
        elif (inp == 0):
            print("Thankyou for using the service.")
            print("You have been logged out.")
            break
    else:
            print('Please enter a valid option')

#if authentication fails, an error message will be displayed
elif (not(user_1.check(username, password))):
    print('Please input a valid 4-digit PIN')