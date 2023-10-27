import click
from os.path import exists
import json
from prettytable import PrettyTable
@click.group()
def cli():
    pass

def PrintBanner():
    banner=r''' 
    ,ggggggggggg,  ,ggggggggggg,                                     ,gggg,       ,gggg,
dP"""88""""""Y8dP"""88""""""Y8,                     ,dPYb,      ,88"""Y8b,    d8" "8I
Yb,  88      `8Yb,  88      `8b                     IP'`Yb     d8"     `Y8    88  ,dP
 `"  88      ,8P`"  88      ,8P                     I8  8I    d8'   8b  d8 8888888P"
     88aaaad8P"     88aaaad8P"                      I8  8bgg,,8I    "Y88P'    88
     88"""""        88""""Y8ba   ,ggggg,   ,ggggg,  I8 dP" "8I8'              88
     88             88      `8b dP"  "Y8ggdP"  "Y8ggI8d8bggP"d8          ,aa,_88
     88             88      ,8Pi8'    ,8Ii8'    ,8I I8P' "Yb,Y8,        dP" "88P
     88             88_____,d8,d8,   ,d8,d8,   ,d8',d8    `Yb`Yba,,_____Yb,_,d88b,,
     88            88888888P" P"Y8888P" P"Y8888P"  88P      Y8 `"Y8888888"Y8P"  "Y88888
                                                                                       
                                                                                       
                                                                                       
          Version 1.0 | Manage your contact records | Made by LowKey          
                                                                                       
'''
    print(banner)
@cli.command()
@click.option("-f","--filen",help="File name")
def createphonebook(filen):
    file_name=filen
    data=[]
    while exists(file_name):
        file_name=input("file name already exists! \nEnter new file name: ")
    with open(file_name,'w') as phonebook:
        instance=[]
        json.dump(instance, phonebook)
    count=0
    ch=input("do you want to enter the data as well(YES/NO)").lower()
    if ch=="yes":
        print('press "ctrl+c" to save and exit the program')
        while True:
            try:
                name= input(f"name(no. {count+1}): ")
                phonenumber=int(input("phonenumber: "))
                user={"name":name,
                "phone":phonenumber}
                data.append(user)
                count+=1
            except KeyboardInterrupt:
                print("\nsaving the data...")
                with open(file_name,'w') as phonebook:
                    json.dump(data, phonebook)
                print("data saved :)")
                print("[*] exiting the program|")
                break


@cli.command()
@click.option("-f","--filen",help="File name")
def showdata(filen):
    while not exists(filen):
        filen=input(f"'{filen}' does not exist\nre-enter the name:")
    with open(filen,'r') as phonebook:
        data=json.load(phonebook)
        
    table=PrettyTable()
    table.field_names=["Sno.","Name","Phone-number"]
    for index,entry in enumerate(data,start=1):
        table.add_row([index,entry["name"],entry["phone"]])
    print(table)

@cli.command()
@click.option("-f","--filen",help="File name")
@click.option("-n","--name",help="name in entry")
@click.option("-pn","--phone",help="phone-number in an entry")
def search(filen, name, phone):
    with open(filen,'r') as p:
        phonebook=json.load(p)

    found_entries=[]
    for entry in phonebook:
            if (phone and entry["phone"]==int(phone)) or (name and entry["name"]==name):
                found_entry=entry
                found_entries.append(found_entry)
            else:
                continue
    table=PrettyTable()
    table.field_names=["Sno.","Name","Phone-No."]
    for index,entries in enumerate(found_entries, start=1):
        table.add_row([index,entries["name"],entries["phone"]])

    print(table)
    
@cli.command()
@click.option("-f","--filen",help="File name")
@click.option("-n","--name",help="name in entry")
@click.option("-i","--index", help="index of the entry")
@click.option("-pn","--phone",help="phone-number in an entry")
def delete(filen, name, phone,index):
    with open(filen,'r') as p:
        phonebook=json.load(p)
    to_delete=[]
    for i,entry in enumerate(phonebook, start=1):
            if (phone and entry["phone"]==int(phone)) or (name and entry["name"]==name) or (index and i==index):
                to_delete.append(i)
    deleted=[]
    if to_delete:
        for i in reversed(to_delete):
            deleted.append(phonebook[i-1])
            del phonebook[i-1]
    if deleted:
        with open(filen, "w") as f:
            json.dump(phonebook, f)
        table=PrettyTable()
        table.field_names=["Sno.","Name","Phone no."]
        for i, entry in enumerate(deleted, start=1):
            table.add_row([i,entry["name"],entry["phone"]])
        print(f"These entries were deleted\n{table}")
    else:
        print("[*] No matching entries were found :(")
if __name__=="__main__":
    PrintBanner()
    cli()
