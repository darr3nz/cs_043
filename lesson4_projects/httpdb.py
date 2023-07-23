class Simpledb:
    def __init__(self, filename):
        self.filename = filename
        f = open(filename, "w")
        f.close()

    def __repr__(self):
        return ("<" + self.__class__.__name__ +
        " file=" + str(self.filename) +
        ">")

# This function will add someone's phone number and name to the database
    def add(self, name, phone_number):
        f = open(self.filename, "a")
        f.write(name + "\t" + phone_number + "\n")
        f.close()

# This function will find a name then will tell you their phone number on the server
    def find(self, find_name):
        f = open(self.filename, "r")
        for row in f:
            (name, phone) = row.split("\t", 1)
            if name == find_name:
                f.close()
                return phone
        return ''

# This function will delete a name and phone number from the database
    def delete(self, delete_name):
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
            return False
        else:
            return True

    # This function will update a name and phone number from the database
    def update(self, update_name, update_phone_number):
        f = open(self.filename, "r")
        result = open('resultdirectoryfile.txt', "w")
        found = False
        for row in f:
            (name, phone) = row.split("\t", 1)
            if name == update_name:
                result.write(update_name + '\t' + update_phone_number + '\n')
                found = True
            else:
                result.write(row)
        f.close()
        result.close()
        import os
        os.replace("resultdirectoryfile.txt", self.filename)
        return found
