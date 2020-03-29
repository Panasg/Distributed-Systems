# This is the CLI ( Command Line Interface ) for the user..

import argparse
# Argparse figures how to parse the given arguments
import settings
# Settings declare the capacity and difficulty variables
import requests
# Elegant and siple HTTP library
import os
# OS module provides a way of using operating system dependent functionality
import sys
# Provides access to system-specific variables and functions


help_msg =
'''
Usage:
Commands:
--> 't <recipient_address> <amount>'  ---  Choose this command to create a new transaction
--> 'view'                            ---  Choose this command to view last transactions
--> 'balance'                         ---  Choose this command to show the balance
--> 'help || -h'                      ---  Choose this command to get yourself some help ASAP
--> 'exit'                            ---  Choose this command to exit client mode
'''


'''Welcome back AlexDeGreek'''


# Initialize the parser
parser = argparse.ArgumentParser(description = 'Greatest CLI ever built')

# Adding arguments
parser.add_argument('host',type='str',metavar='',help='Current Hostname to be announced to the Coordinator')
parser.add_argument('port',type='int',metavar='',help='Port used by the current user')

# Execute the parse_args() method
args = parser.parse_args()

#COORDINATOR_HOST=f'http://{args.host}:{args.port}'
HOST=f'http://127.0.0.1:{args.port}'
PORT=str(args.port)


# Main Loop

while True:
    cmd = input(">> ")
    print(cmd)
    if cmd == 'exit' :
        break   # Time to exit our loop
    elif cmd == 'help' or cmd =='-h' :
        print(help_msg) # User needs some help
    elif  cmd == 'balance' :
        wallet_balance = requests.get(f'{HOST}/wallet_balance').json() # Get the wallet's current balance
        for balance in wallet_balance:
            print(sum((balance))    # Print the sum of the UTXOs
    elif cmd == 'view' :
        view_latest_transactions = requests.get(f'{HOST}/view_transactions').json()  # Get the latest transaction of the block
        for transaction in view_latest_transactions:
        #    print(f'{transaction["sender"]}{transaction["recipient"]}{transaction["amount"]}{transaction["index"]}) # Print Sender/Recipient/Amound/Index
    elif cmd == cmd.startswith('t'):
        part = cmd.split();
        # Time to create a new transaction

        try:

        if response.status_code == 200: # Everthing is well done
            print("Transaction Completed!")
        else:
            print("Error occured")  # Some error occured in creating the new transaction
    else :
        print("This command is unknown. For further help call 'help' command")  # Command unknown. For further development please support us on Patreon

# This is the end of the CLI
