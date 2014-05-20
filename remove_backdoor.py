#!/usr/bin/env python3

import sys, telnetlib, getpass

print("\n\nActionTec GT704WG\nISP Backdoor Removal Tool\n\nRemoves the ISP hardcoded backdoor on port 4567 and the web activity log.\n\n\n")
print("NOTE: You can leave the Router IP Address, Username, or Password blank to use the defaults.\n")
print("Default Router IP Address: 192.168.1.1\nDefault Username: admin\nDefault Password: password\n\n")

# define our routers ip, username, and password
ip = input("\nRouter IP Address: ")
username = input("Username: ")
password = getpass.getpass()
if ip == "":
    ip = "192.168.1.1"
if username == "":
    username = "admin"
if password == "":
    password = "password"

# connect to the router and log in
def routerConnect():
    tn.read_until(b"login:")
    tn.write(username.encode("ascii") + b"\n")
    tn.read_until(b"Password:")
    tn.write(password.encode("ascii") + b"\n")
   
# read IP tables data
def ipTablesRead():
    tn.write(b"iptables -L -t nat\n")
   
# delete the web activity log, and redirect it to dev/null
def deleteActivityLog():
    tn.write(b"cd /var/tmp\n")
    tn.write(b"rm log_web_activity\n")
    tn.write(b"ln -s /dev/null log_web_activity\n")
    print("Web activity log was removed successfully\n\n\n")

# begin script, first connect to the router and read the IP Tables data
try:

    # make the initial connection and read IPTables data
    tn = telnetlib.Telnet(ip)
    routerConnect()
    ipTablesRead()
    tn.write(b"exit\n")
    
    # store the IPTables output in a variable
    output = tn.read_all().decode("ascii")
    
    # reconnect and prepare to modify router settings based on the output variable
    tn = telnetlib.Telnet(ip)
    routerConnect()

    # check if the ISP backdoor port 4567 is being forwarded in IP Tables
    if "dpt:4567" in output:
        print("\n\n\nISP backdoor has been detected!!!")
        tn.write(b"iptables -t nat -D PREROUTING 1\n")
        print("ISP Backdoor was removed successfully")
        deleteActivityLog()    
    else:
        print("\n\n\nISP backdoor is not active, it has already been removed")
        deleteActivityLog()

    tn.write(b"exit\n")
    tn.close

    input("Router was successfully patched!\n\nPress 'Enter' key to exit...")

except:

    input("\n\nSomething went wrong!\n\nPress 'Enter' key to exit...")
