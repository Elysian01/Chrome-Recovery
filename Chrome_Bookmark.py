import os
import sys
import argparse
import json

def Arguments():
    parser = argparse.ArgumentParser(description = "To Retrieve Google Chrome Bookmark ")
    parser.add_argument("-d","--display",help ="To display the output on the terminal",action = "store_true")
    parser.add_argument ("-o","--output",help = "To save the output in {csv | json | txt } format")
    args = parser.parse_args()

    if args.display :
        for data in Extracter():
            print(data)
    elif args.output == "csv":
        output_csv(Extracter())
    elif args.output == "json":
        output_json(Extracter())
    elif args.output == "txt":
        output_txt(Extracter())
    else:
        parser.print_help()



def Extracter():
    path = getpath()
    path = path + 'Bookmarks'
    info_list = []
    with open(path ,'r') as f:
        with open ("Bookmarks.json","w") as b:
            for line in f:
                b.write(line)

    with open("Bookmarks.json","r") as b:
        contents = b.read()
        # print(type(contents))  --> strings
        data = json.loads(contents)  # --> converts the string into a dictionary to perform operations
        
        bar_length = len(data['roots']['bookmark_bar']['children'])
            
        for i in range(0,bar_length):
                # print(data['roots']['bookmark_bar']['children'][i]['date_added'] , end = "\t\t " ,sep = "\t\t ")
                # print(data['roots']['bookmark_bar']['children'][i]['name'] , end = "\t\t " ,sep = "\t\t ")
                # print(data['roots']['bookmark_bar']['children'][i]['url'] , end = "\t\t " ,sep = "\t\t ")
                # print()
            info_list.append(
                {
                'bookmark_bar' : {
                    "Date_Added" : data['roots']['bookmark_bar']['children'][i]['date_added'],
                    "Name" : data['roots']['bookmark_bar']['children'][i]['name'],
                    "Url" : data['roots']['bookmark_bar']['children'][i]['url']
                    }
                })

        
        syn_length = len(data['roots']['synced']['children'])
        
        for i in range(0,syn_length):
            info_list.append(
            {
            'Synced': {
                "Date_Added" : data['roots']['synced']['children'][i]['date_added'],
                "Name" : data['roots']['synced']['children'][i]['name'],
                "Url" :data['roots']['synced']['children'][i]['url']
                }
            })

    return info_list


os_platform =  sys.platform

def getpath():
    if os_platform == "win32" or "cygwin":
        PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
    else:
        print("Operating System Currently not supported ")

    return PathName

def output_csv(info):
    with open('Chrome_bookmarks.csv','w') as csv_file:
        for line in info:
            csv_file.write(json.dumps(line,indent = 5))
    print("The output stored in Chrome_bookmarks.csv file")


def output_json(info):
    with open('Chrome_bookmarks.json','w') as json_file:
        for line in info:
           json_file.write(json.dumps(line,indent = 5))
    print("The output stored in Chrome_bookmarks.json file")
    

def output_txt(info):
    with open('Chrome_bookmarks.txt','w') as txtfile:
        for line in info:
            txtfile.write(json.dumps(line,indent= 5))
    print("The output stored in Chrome_bookmarks.txt file")

if __name__ == "__main__":
    Arguments()
