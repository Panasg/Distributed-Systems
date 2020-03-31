# This is the CLI ( Command Line Interface ) for the user..

#import argparse
# Argparse figures how to parse the given arguments
import requests
# Elegant and siple HTTP library
import os
# OS module provides a way of using operating system dependent functionality
import sys
# Provides access to system-specific variables and functions
import json
import time

help_msg ="""
Usage:
Commands:
--> 't <recipient_address> <amount>'  ---  Choose this command to create a new transaction
--> 'bulk_transactions'                    ---  Choose this command to import a file of transactions
--> 'view'                            ---  Choose this command to view last transactions
--> 'balance'                         ---  Choose this command to show the balance
--> 'help || -h'                      ---  Choose this command to get yourself some help ASAP
--> 'state'                           ---  Choose this command to get yourself a readable view of all data
--> 'benchmark'                       ---  Choose this command to get benchmark data. Better use when mining has stopped
--> 'exit'                            ---  Choose this command to exit client mode
"""


'''Welcome back AlexDeGreek'''


# Initialize the parser
#parser = argparse.ArgumentParser(description = 'Greatest CLI ever built')

# Adding arguments
#parser.add_argument('host',type='str',metavar='',help='Current Hostname to be announced to the Coordinator')
print(sys.argv)
#parser.add_argument('port',type='int',metavar='',help='Port used by the current user')

# Execute the parse_args() method
#args = parser.parse_args()

#COORDINATOR_HOST=f'http://{args.host}:{args.port}' cli 1 5000
URL=f'http://192.168.0.{sys.argv[1]}:{sys.argv[2]}'
PORT=int(sys.argv[2])
id = int(sys.argv[1])-1

# Main Loop
kwargs = {}
kwargs['timeout'] = 25

while True:
    cmd = input(">> ")
    print(cmd)
    if cmd == 'exit' :
        break   # Time to exit our loop

    elif cmd == 'help' or cmd =='-h' :
        print(help_msg) # User needs some help

    elif  cmd == 'balance' :
        wallet_balance = requests.get(f'{URL}/show_balance').text # Get the wallet's current balance

        print(wallet_balance)   # Print the sum of the UTXOs
    elif cmd == 'view' :
        view_transactions = requests.get(f'{URL}/view_transactions').text  # Get the latest transaction of the block
        print(view_transactions) # Print Sender/Recipient/Amound/Index

    elif cmd.startswith('t'):
        part = cmd.split()
        if int(part[1])==id:
            print("Can't send money to myself")
            continue
        # Time to create a new transaction
        if(int(part[2])<=0):
            print("Money must be a positive value")
            continue
        trans_dict = {'recipient_address': int(part[1]), 'amount': int(part[2])}
        response=requests.post(f'{URL}/new_transaction',json=trans_dict,**kwargs)
        if response.status_code == 200: # Everthing is well done
            print("Transaction Completed!")
        else:
            print("Error occured")  # Some error occured in creating the new transaction

    elif cmd == 'bulk_transactions':
        f = open(f'5nodes/transactions{id}.txt', "r")
        #f = open(f'transactions{id}.txt', "r")
        for x in f:
            part = x.split(' ')
            recepient = int((part[0].split('id'))[1])
            if recepient==id:
                print("Can't send money to myself")
                continue
            amount=int(part[1])
            trans_dict = {'recipient_address': recepient, 'amount': amount}
            kwargs['timeout'] = 25
            response=requests.post(f'{URL}/new_transaction',json=trans_dict,**kwargs)
            if response.status_code == 200: # Everthing is well done
                print("Transaction Completed!")
            else:
                print("Error occured")  # Some error occured in creating the new transaction
        f.close()

    elif cmd=='state':
        print(requests.get(f'{URL}/cliShowMeYourState').text)
    elif cmd=='benchmark':
        print(requests.get(f'{URL}/benchmark').text)

    else :
        print("This command is unknown. For further help call 'help' command")  # Command unknown. For further development please support us on Patreon

# This is the end of the perfect CLI
