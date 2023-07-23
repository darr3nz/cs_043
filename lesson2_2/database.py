# This function asks you to input a name and their phone number and will add it to the bottom of the directory
class Simpledb:
    def __init__(db, filename):
        db.filename = filename
        f = open(filename, "w")
        f.close()

    def __repr__(self):
        return ("<" + self.__class__.__name__ +
        " file=" + str(self.filename) +
        ">")

    def add(self):
        name = input("\nWhat is the name of the person you are adding? \nEnter their first and last name: ")
        phone_number = input("What is the phone number of the person you are adding? \nEnter phone number: ")
        f = open(self.filename, "a")
        f.write(name + "\t" + phone_number + "\n")
        f.close()
        print("\nMessage: " + name + " was added to the directory.\n")

    # This function will ask you what name you would want to find in the directory and it will tell you the phone number if found
    def find(self):
        find_name = input("\nWhat is the name of the person you are looking for? \nEnter their first and last name: ")
        f = open(self.filename, "r")
        for row in f:
            (name, phone) = row.split("\t", 1)
            if name == find_name:
                print("\nMessage: Found " + find_name + "'s phone number. It is " + phone + "\n")
                f.close()
                return
        print("\nMessage: We couldn't find " + find_name + "'s phone number in the directory.\n")

    # This function will ask you for a name to delete and if it finds it, it would delete their name and phone number from the directory
    def delete(self):
        delete_name = input("\nWho do you want to delete from your phone directory?\nEnter their first and last name: ")
        f = open(self.filename, "r")
        result = open('resultdirectoryfile.txt', "w")
        found = False
        for row in f:
            (name, phone) = row.split("\t", 1)
            if name == delete_name:
                found = True
            else:
                result.write(row)
        f.close()
        result.close()
        import os
        os.replace("resultdirectoryfile.txt", self.filename)
        if found == False:
            print("\nMessage: " + delete_name + " is not found in the directory.\n")
        else:
            print("\nMessage: We found and deleted " + delete_name + " from the directory.\n")

    # This function will ask you for a name and if it finds the name, it would ask you for the new phone number and will update it.
    def update(self):
        update_name = input("\nWhat is the name of the person to be updated?\nEnter their first and last name: ")
        f = open(self.filename, "r")
        result = open('resultdirectoryfile.txt', "w")
        found = False
        for row in f:
            (name, phone) = row.split("\t", 1)
            if name == update_name:
                update_phone_number = input("What is " + name + "'s new phone number?\nEnter new phone number: ")
                result.write(update_name + '\t' + update_phone_number + '\n')
                found = True
            else:
                result.write(row)
        f.close()
        result.close()
        import os
        os.replace("resultdirectoryfile.txt", self.filename)
        if found == False:
            print("\nMessage: " + update_name + " is not found in the directory therefore we can't update their phone number.\n")
        else:
            print("\nMessage: We found and updated " + update_name + "'s phone number.\n")
