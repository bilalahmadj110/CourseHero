import platform
import os
def user_groups(fout):
    print("USERS: ")
    print (f"  Executing `cat /etc/passwd > users.txt`")
    os.system("cat /etc/passwd > users.txt")
    # Storing the users in a temporary file
    try:
        f = open('users.txt')
    except FileNotFoundError:
        print("  File is not present")
    lines = f.readlines()
    userslist = []
    for line in lines:
        userslist.append(line.split(":")[0])
    f.close()
    print (f"  Users found: {len(userslist)}")
    # Writing the fetched users to output file
    fout.write("\nUSER GROUPS:\n")
    for user in userslist:
        print (f"    Executing `groups {user} > usergroups.txt\`")
        os.system(f"groups {user} > usergroups.txt")
        try:
            f_temp = open('usergroups.txt')
        except FileNotFoundError:
            print("    File is not present")
        line = f_temp.readline().strip().split(':')
        # User
        usr = line[0]
        # Groups associated to this user
        groups = line[1].strip().split(" ")
        f_temp.close()
        # Writing user
        fout.write(usr + str(": \n"))
        # Writing groups associated to this user
        for grp in groups:
            fout.write("\t" + str(grp) + "\n")


def processors(fout):
    print ("PROCESSORS:")
    fout.write("\nPROCESSORS: \n")
    print (f"  Executing `cat /proc/cpuinfo > cpuinfo.txt`")
    os.system('cat /proc/cpuinfo > cpuinfo.txt')

    try:
        f_proc = open('cpuinfo.txt')
    except FileNotFoundError:
        print ('  File is not present')

    lines = f_proc.readlines()
    processors = []
    temp_dict = {}
    for line in lines:
        if line == '\n':
            processors.append(temp_dict)
            temp_dict = {}
        temp_line = line.strip().split(":")
        if temp_line[0].strip() == "processor":
            temp_dict["Processor"] = temp_line[1].strip()
        if temp_line[0].strip() == "vendor__id":
            temp_dict["Vendor_id"] = temp_line[1].strip()
        if temp_line[0].strip() == "model":
            temp_dict["Model"] = temp_line[1].strip()
        if temp_line[0].strip() == "model name":
            temp_dict["Model_name"] = temp_line[1].strip()
        if temp_line[0].strip() == "cache size":
            temp_dict["Cache"] = temp_line[1].strip()

    for processor in processors:
        for key,value in processor.items():
            fout.write(f"(key): {value} \n")
            fout.write("\n")


def services(fout):
    print ("SERVICES:")
    fout.write("SERVICES: \n")
    fout.write("SERVICE STATUS \n")
    print (f'  Executing `systemctl list-units --type=service > services.txt`')
    os.system("systemctl list-units --type=service > services.txt")

    # Writing the serv. info
    try:
        f_services = open("services.txt")
    except FileNotFoundError:
        print ("  Service file not present")
    line = f_services.readline()
    while line != '\n':
        fout.write(line)
        line = f_services.readline()
    f_services.close()
    

def main():                                     
    fout = open("output.txt", "+a")
    fout.write("\nMACHINE NAME: " + str(platform.node()) + "\n")
    user_groups(fout)
    processors(fout)
    services(fout)
    fout.close()
    
main()
