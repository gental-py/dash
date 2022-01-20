import getpass, os

def cls():
    os.system("cls")

def read(loc):
    file = open(loc, "r")
    content = file.read()
    return content


_OsUsername_ = getpass.getuser()

class Location:
    private = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\logs\\private.log"
    public = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\logs\\public.log"

last_log = ""
while True:
    NewRead = read(Location.public)

    if NewRead != last_log:
        cls()
        print(NewRead)
        last_log = NewRead

