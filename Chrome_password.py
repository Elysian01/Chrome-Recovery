import argparse
import os
import sys
import sqlite3
import csv
import json

try:
    import win32crypt       # Since chrome store all chrome password using a randomly generated key  
except:
    pass


def Arguments():
    parser = argparse.ArgumentParser(description = "Retrieve Google Chrome Saved Passwords")
    parser.add_argument('-o','--output',help = "Enter the format [ csv | json | text ] in which you wanna save file")
    parser.add_argument('-d','--display',help = "To display the output in terminal",action = 'store_true')
    args = parser.parse_args()

    if args.display :
        for data in Extracter():
            print(data)
    elif args.output == "csv":
        output_csv(Extracter())
    elif args.output == "json":
        output_json(Extracter())
    elif args.output == "text":
        output_text(Extracter())
    else:
        parser.print_help()   
    

def Extracter():

    info_list = []
    path = getpath()

    try:
        connection = sqlite3.connect(path + 'Login Data')    # Setting path to DB
        with connection:
            cursor = connection.cursor()
            v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')  #SQL Command
            value = v.fetchall()  #Collect and store all rows

            for url,username,password in value :

                if password:
                    password = win32crypt.CryptUnprotectData(password,None,None,None,0)
        
                info_list.append({
                    "Origin_Url" : url,
                    "Username" : username,
                    "Password" : str(password) 
                })
    except sqlite3.OperationalError as e:
        e = str(e)
        if (e == 'database is locked'):
            print('[!] Make sure Google Chrome is not running in the background')
        elif (e == 'no such table: logins'):
            print('[!] Something wrong with the database name')
        elif (e == 'unable to open database file'):
            print('[!] Something wrong with the database path')
        else:
            print(e)
        sys.exit(0)

    return info_list

def getpath():

    if os.name == 'nt':       # for Windows
        PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
    
    elif os.name == 'posix':    # for OS X
        print("Currently Platform not supported ")
        sys.exit()
    else :               # Else for Linux User
        path = '/.config/google-chrome/Defaults '
    
    return PathName

def output_csv(info):
    try:
        with open('Chrome_password.csv','wb') as csv_file:
            for data in info:
                csv_file.write(f"{data['Origin_Url']}\t\t {data['Username']}\t\t {data['Password']}\n".encode('utf-8'))
        
        print("Data written to Chrome_passwords.csv")
    except EnvironmentError:
        print("Environmental error connot write data")
            
# Python uses UNICODE() > 256 CHARACTER BUT OTHER APPLICATION DON'T UNDERSTAND UNICODE THEREFORE WE HAVE TO ENCODE IT USING UTF-8
# UTF-8 IS STANDARD CODING
# UNICODE HAS CODE FOR EACH CHARACTER IN EVERY LANGUAGE LIKE JAPANESE,GERMAN,BRITISH,ETC

def output_json(info):
    with open('Chrome_password.json','wb') as json_file:
        for data in info:
            json_file.write(f"{data['Origin_Url']} \t\t {data['Username']} \t\t{data['Password']} \n".encode('utf-8'))  # encode convert string into bytes
    print("Data Successfully written in Chrome_password.json")

def output_text(info):
    with open('Chrome_password.txt','wb') as txt_file:
        for data in info:
            txt_file.write(f"{data['Origin_Url']} \t\t {data['Username']} \t\t{data['Password']} \n".encode('utf-8'))  # encode convert string into bytes
    print("Data Successfully written in Chrome_password.txt")
    

if __name__ == '__main__':
    Arguments()