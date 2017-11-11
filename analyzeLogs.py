import os
import re
import sys

def read_logs(path, number_files):
    all_contents = "" # string that will contain all logs
    for files in range(0, number_files): # iterate over all files
        if files == number_files:
            break
        if files == 0:
            fn = path
        else:
            fn = path + "." + str(files)
        fl = open(fn, "r")
        for line in fl: # iterate over all lines in a single file
            all_contents += line # add line to all_contents
        fl.close()
    result = open("allLogs.txt", "w") # create file allLogs.txt
    result.write(all_contents)
    result.close()

def analyze_auth_logs():
    logs = open("allLogs.txt")
    usernames = []
    # regex that matches the line starting with "Failed password for .." and groups usernames and ip adress
    p1 = re.compile(".* Failed password for ((invalid user (\w+))|((?!invalid user)(\w+))) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .*")
    count = {}
    for line in logs: # iterate over each line
        match = p1.match(line) # match line with regex
        if match is not None: # if there is a match do following
            match_index = None # initialize match index. Can be of group3 or group4 depending on match
            if len(usernames) == 0: # if usernames is empty, directly add this user and ip
                if match.group(3) is not None:
                    match_index = 3
                elif match.group(4) is not None:
                    match_index = 4
                usernames.append(match.group(match_index))
                count[match.group(match_index)] = {}
                count[match.group(match_index)]["count"] = 1
                count[match.group(match_index)]["ip"] = []
                count[match.group(match_index)]["ip"].append(match.group(6)) 
            else: # if usernames is not empty check if username already exists
                exists = False
                if match.group(3) is not None:
                    match_index = 3
                elif match.group(4) is not None:
                    match_index = 4
                for name in usernames:
                    if name == match.group(match_index): # if username already exists, increase count and add ip
                        exists = True
                        count[match.group(match_index)]["count"] += 1
                        ip_exists = False
                        for i in count[match.group(match_index)]["ip"]: # check if ip already exists. If not, add ip
                            if match.group(6) == i:
                                ip_exists = True
                                break
                        if not ip_exists:
                            count[match.group(match_index)]["ip"].append(match.group(6))
                        break
                if not exists: # if user does not exists yet, add username and ip
                    usernames.append(match.group(match_index))
                    count[match.group(match_index)] = {}
                    count[match.group(match_index)]["count"] = 1
                    count[match.group(match_index)]["ip"] = []
                    count[match.group(match_index)]["ip"].append(match.group(6))
        
    logs.close()
    os.remove("allLogs.txt")
    output = "User;LoginAttempts;IPs\n" # create header for .csv
    for key in count: # iterate over all users and add name, count and IPs to output string
        output += key + ";" + str(count[key]["count"]) + ";"
        for i in range(len(count[key]["ip"])):
            if i == len(count[key]["ip"])-1:
                output += str(count[key]["ip"][i]) + "\n"
            else:
                output += str(count[key]["ip"][i]) + "," 
    authlist = open("authlist.csv", "w") # create empty authlist.csv
    authlist.write(output) # add text to authlist.csv
    authlist.close()

##### Main #######
path = sys.argv[1]
n_files = sys.argv[2]
read_logs(path, int(n_files))
analyze_auth_logs()
print "Analysis complete. Results in " + os.getcwd() + "/authlist.csv"
