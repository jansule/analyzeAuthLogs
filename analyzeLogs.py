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
    auths = ""
    usernames = []
    p1 = re.compile(".* Failed password for ((invalid user (\w+))|((?!invalid user)(\w+))) from .*")
    count = {}
    for line in logs:
        match = p1.match(line)
        if match is not None:
            auths += line
            match_index = None
            if len(usernames) == 0:
                if match.group(3) is not None:
                    match_index = 3
                elif match.group(4) is not None:
                    match_index = 4
                usernames.append(match.group(match_index))
                count[match.group(match_index)] = 1
            else:
                exists = False
                if match.group(3) is not None:
                    match_index = 3
                elif match.group(4) is not None:
                    match_index = 4
                for name in usernames:
                    if name == match.group(match_index):
                        exists = True
                        count[match.group(match_index)] += 1
                        break
                if not exists:
                    usernames.append(match.group(match_index))
                    count[match.group(match_index)] = 1
        
    logs.close()
    os.remove("allLogs.txt")
    output = "User,LoginAttempts\n"
    for key in count:
        output += key + "," + str(count[key]) + "\n"
    authlist = open("authlist.csv", "w")
    authlist.write(output)
    authlist.close()

##### Main #######
path = sys.argv[1]
n_files = sys.argv[2]
read_logs(path, int(n_files))
analyze_auth_logs()
print "Analysis complete. Results in " + os.getcwd() + "/authlist.csv"
