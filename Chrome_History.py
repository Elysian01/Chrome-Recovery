import os
import sys 
import argparse
import sqlite3


def Arguments():
    parser = argparse.ArgumentParser(description = "Retrieve Google Chrome Histroy ")
    parser.add_argument("-d","--display",help ="To display the output on the terminal",action = "store_true")
    parser.add_argument ("-o","--output",help = "To save the output in {csv | json | text } format")
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


os_Platform = sys.platform
        
def getpath():
    if os_Platform =="win32" or os_Platform == "cygwin":
        PathName = os.getenv("localappdata") + '\\\Google\\Chrome\\User Data\\Default\\'
    else:
        if os_Platform == "linux" or os_Platform == "linux2":
            PathName = '/.config/google-chrome/Defaults '
        else:
            print("Currently Operating System Not Supported")
    return PathName


def Extracter(): 
    path = getpath()
    info_list = []
    try:
        connection = sqlite3.connect(path + 'History')
        with connection:   # Context Manager
            cursor = connection.cursor()
            v = cursor.execute("""SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') 
                                    AS last_visit_time FROM urls ORDER BY last_visit_time DESC""")
            value = v.fetchall()
        
            for url,title,last_visit_time in value:
                info_list.append({
                    "Url": url,
                    "Title": title,
                    "Date&Time":last_visit_time 
                })
    except sqlite3.OperationalError as e:
        print(e)
    return info_list
def output_csv(info):
    with open('Chrome_history.csv','wb') as csv_file:
        for data in info:
            csv_file.write(f"{data['Url']} \t {data['Title']} \t {data['Date&Time']} \n".encode('UTF-8'))
    print("Write Successfull , file stored as Chrome_history.csv")

def output_json(info):
    with open('Chrome_history.json','wb') as json_file:
        for data in info:
            json_file.write(f"{data['Url']} \t\t {data['Title']} \t\t{data['Date&Time']} \n".encode('utf-8'))  # encode convert string into bytes
    print("Data Successfully written in Chrome_history.json")

def output_text(info):
    with open('Chrome_history.txt','wb') as txt_file:
        for data in info:
            txt_file.write(f"{data['Url']} \t\t {data['Title']} \t\t{data['Date&Time']} \n".encode('utf-8'))  # encode convert string into bytes
    print("Data Successfully written in Chrome_history.txt")
    


if __name__ == "__main__":
    Arguments()
