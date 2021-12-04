print("  [Info] Import packeges : ", end="")
import os, platform, sys, subprocess, getpass, datetime, socket, requests, getmac, pyperclip, configparser as cp
print("OK")

# System username
_OsUsername_ = getpass.getuser()

# Files
print("  [Info] Configuring configparser : ", end="")
VarsCP = cp.ConfigParser()
ConfigCP = cp.ConfigParser()
RegistryCp = cp.ConfigParser()
CommandsCp   = cp.ConfigParser()

Vars_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\vars.dash"
Config_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\config.dash"
Registry_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\reg.dash"
MainFolder_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\"
Commands_Loc     = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\commands.dash"

VarsCP.read(Vars_Loc)
ConfigCP.read(Config_Loc)
RegistryCp.read(Registry_Loc)
print("OK")

print("  [Info] Checking files : [", end="")
if not os.path.exists(MainFolder_Loc):
    os.mkdir(MainFolder_Loc)
    print("main,",end="")
if not os.path.exists(Vars_Loc):
    open(Vars_Loc, "a+").close()
    print("vars,",end="")
if not os.path.exists(Commands_Loc):
    open(Commands_Loc, "a+").close()
    print("commands,",end="")
if not os.path.exists(Config_Loc) or os.path.getsize(Config_Loc) == 0:
    open(Config_Loc, "a+").close()

    ConfigCP["customization"] = {"name": "dash", "cursor": "•", "sepchar": "."}
    with open(Config_Loc, "w") as file:
        ConfigCP.write(file)
    print("config,",end="")
if not os.path.exists(Registry_Loc) or os.path.getsize(Registry_Loc) == 0:
    open(Registry_Loc, "a+").close()
    RegistryCp["reg"] = {"checkPlatform": "true", "checkArgLenght": "true", "spaceBeetwenCursor": "true", "enableColors": "true", "copyOutput": "false", "startAsRoot": "false", "showBootupInfo": "false", "enablecustomcommands": "true"}
    with open(Registry_Loc, "w") as file:
        RegistryCp.write(file)
    print("reg",end="")
print("] : OK")

# Check if program is running on windows.
print("  [Info] Checking platform : ",end="")
if RegistryCp["reg"]["checkPlatform"] == "true":
    if platform.system() != "Windows":
        print("  Hi user. Propably dash should run on windows. You can force that by changing \"checkplatform\" entry.")
        exit()
print("OK")

# Colors
print("  [Info] Setting up colors : ",end="")
if not __import__("sys").stdout.isatty():
    for _ in dir():
        if isinstance(_, str) and _[0] != "_":
            locals()[_] = ""
else:
    if platform.system() == "Windows":
        kernel32 = __import__("ctypes").windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        del kernel32
print("OK")

# Functions
def Cls():
    os.system("cls || clear")
    print("\n")

def ClearOneLine():
    print("\033[A                                                             \033[A")

def ListToString(InList):
    DoneStr = ""
    for Element in InList:
        DoneStr += Element
    return DoneStr

# Configuration
def ReadUserConfig():
    ConfigCP.read(Config_Loc)
    _SepChar = ConfigCP["customization"]["sepchar"]
    _Cursor = ConfigCP["customization"]["cursor"]
    _Name = ConfigCP["customization"]["name"]

    return (_Name, _Cursor, _SepChar)

def ReadUserVariables():
    VarsCP.read(Vars_Loc)

def TurnColors():
    global end, red, gray, green

    RegistryCp.read(Registry_Loc)
    if RegistryCp["reg"]["enableColors"] == "false":
        end = ""
        red = ""
        gray = ""
        green = ""

# Format input
def FormatInput(UserInput):

    FormatInput_sep = ReadUserConfig()[2]
    if FormatInput_sep == "_":
        FormatInput_sep = " "
 
    UserInputList = UserInput.split(FormatInput_sep)
    UserInputList[0] = UserInputList[0].replace(" ", "").lower()

    return UserInputList


# Select mode
print("  [Info] Setting mode : ",end="")
_Mode_ = str
if RegistryCp["reg"]["startAsRoot"] == "true":
    _Mode_ = "root" 
else:
    _Mode_ = "nrml"
print("OK")

if RegistryCp["reg"]["showBootupInfo"] == "true":
    os.system("pause")


#  Main loop
Cls()
while True:

    # Read user config
    VarsCP.read(Vars_Loc)
    ConfigCP.read(Config_Loc)
    RegistryCp.read(Registry_Loc)
    CommandsCp.read(Commands_Loc)
    UserConfig_Read = ReadUserConfig()
    
    end   = "\033[0m"
    red   = "\033[1;31m"
    gray  = "\033[1;30m"
    green = "\033[1;32m"
    TurnColors()

    class UserConfig:
        Name = UserConfig_Read[0]
        Cursor = UserConfig_Read[1]
        Sepchar = UserConfig_Read[2]

    # Main input
    if RegistryCp["reg"]["spaceBeetwenCursor"] == "true":
        SpaceAfterCursor = " "
    else:
        SpaceAfterCursor = ""

    __Command__ = input(f"({_Mode_}) {UserConfig.Name} {gray}{UserConfig.Cursor}{end}{SpaceAfterCursor}")
    CommandContent = __Command__
    __Command__ = FormatInput(__Command__)

    ClearOneLine()
    print(f"({_Mode_}) {UserConfig.Name} {green}{UserConfig.Cursor}{end}{SpaceAfterCursor}{CommandContent}")

    _CustomCommandsList_ = CommandsCp.sections()

    if __Command__[0]   == "exit":
        exit()

    elif __Command__[0] == "restart":
        os.system("py dash.py")
        exit()

    elif __Command__[0] == "cls":
        Cls()

    elif __Command__[0] == "testarg":
        for i, arg in enumerate(__Command__):
            print(f"  [{i}] = \"{arg}\"")
        print("\n")

    # Settings
    elif __Command__[0] == "mycfg":
        print(f"  Name      ==  \"{UserConfig.Name}\"")
        print(f"  Cursor    ==  \"{UserConfig.Cursor}\"")
        print(f"  Sepchar   ==  \"{UserConfig.Sepchar}\"\n")

    elif __Command__[0] == "set.name":
        try:
            setname_Arg = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_name_>{end}\n")
            continue

        if setname_Arg.replace(" ", "") == "":
            print(f"  {red}Missing argument: <_name_>{end}\n")

        if RegistryCp["reg"]["checkArgLenght"] == "true":
            if len(setname_Arg) > 31:
                print(f"  {red}Argument error: <_name_> is too long. [MaxLen=30]{end}\n")
                continue
            
            if len(setname_Arg) == 0:
                print(f"  {red}Argument error: <_name_> is short. [MinLen=1]{end}\n")
                continue

        ConfigCP["customization"]["name"] = setname_Arg
        with open(Config_Loc, "w") as f:
            ConfigCP.write(f)

    elif __Command__[0] == "set.cursor":
        try:
            setcursor_Arg = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_cursor_>{end}\n")
            continue

        if setcursor_Arg.replace(" ", "") == "":
            print(f"  {red}Missing argument: <_cursor_>{end}\n")

        if RegistryCp["reg"]["checkArgLenght"] == "true":
            if len(setcursor_Arg) > 6:
                print(f"  {red}Argument error: <_cursor_> is too long. MaxLen=5{end}\n")
                continue

            if len(setcursor_Arg) == 0:
                print(f"  {red}Argument error: <_cursor_> is short. [MinLen=1]{end}\n")
                continue

        ConfigCP["customization"]["cursor"] = setcursor_Arg
        with open(Config_Loc, "w") as f:
            ConfigCP.write(f)

    elif __Command__[0] == "set.sepchar":
        try:
            setsepchar_Arg = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_sepchar_>{end}\n")
            continue

        if RegistryCp["reg"]["checkArgLenght"] == "true":
            if len(setsepchar_Arg) > 4:
                print(f"  {red}Argument error: <_sepchar_> is too long. [MaxLen=3]{end}\n")
                continue

        ConfigCP["customization"]["sepchar"] = setsepchar_Arg
        with open(Config_Loc, "w") as f:
            ConfigCP.write(f)

    # Network
    elif __Command__[0] == "netinfo":
        try:
            netinfo_PrivateIP = socket.gethostbyname(socket.gethostname())
            netinfo_PublicIP  = requests.get('https://api.ipify.org').text
            netinfo_PcName    = socket.gethostname()
            netinfo_MacAddr   = getmac.get_mac_address()

            print(f" - IP:\n  Public  {green}>{end} {netinfo_PublicIP}\n  Private {green}>{end} {netinfo_PrivateIP}\n  Mac     {green}>{end} {netinfo_MacAddr}\n")
            print(f" - NAME:\n  This pc {green}>{end} {netinfo_PcName}\n")


        except:
            print(f"  {red}Loading informations Error{end}\n")

        print("")

    elif __Command__[0] == "dnslkp":
        try:
            dnslkp_Addres = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_addres_>{end}\n")
            continue

        dnslkp_Addres = dnslkp_Addres.replace(" ", "")

        try:
            dnslkp_outputIP = socket.gethostbyname(dnslkp_Addres)
            print(f"  IP {green}>{end} {dnslkp_outputIP}", end="")

            RegistryCp.read(Registry_Loc)
            if RegistryCp["reg"]["copyOutput"] == "true":
                pyperclip.copy(dnslkp_outputIP)
                print(f"  {gray}(copied.){end}")
        
        except:
            print(f"  {red}Cannot find out ip addres for: {end}{dnslkp_Addres}\n")

        print("")

    elif __Command__[0] == "revdnslkp":
        try:
            revdnslkp_Addres = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_addres_>{end}\n")
            continue

        revdnslkp_Addres = revdnslkp_Addres.replace(" ", "")

        try:
            revdnslkp_outputIP = socket.gethostbyaddr(revdnslkp_Addres)
            print(f"  IP {green}>{end} {revdnslkp_outputIP[0]}", end="")

            RegistryCp.read(Registry_Loc)
            if RegistryCp["reg"]["copyOutput"] == "true":
                pyperclip.copy(revdnslkp_outputIP[0])
                print(f"  {gray}(copied.){end}")
        
        except:
            print(f"  {red}Cannot find addres for: {end}{revdnslkp_Addres}\n")
        print("")

    # Mode
    elif __Command__[0] == "mode.root":
        _Mode_ = "root"

    elif __Command__[0] == "mode.nrml":
        _Mode_ = "nrml"

    # Registry
    elif __Command__[0] == "regshow":
        RegistryCp.read(Registry_Loc)
        RegistryEntries = RegistryCp.items("reg")

        print("  ==== REGSHOW ====\n")
        for i, entry in enumerate(RegistryEntries):
            print(f"  [{i+1}] |  {green+'T' if entry[1] == 'true' else red+'F'}{end} {entry[0]}")

        print("\n")

    elif __Command__[0] == "regedit":
        if _Mode_ != "root":
            print(f"  {red}This command can be used only as root!{end}\n")
            continue

        try:
            regedit_Name = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_entry.name_> [place: 1]{end}\n")
            continue

        try:
            regedit_NewValue = __Command__[2]
        except:
            print(f"  {red}Missing argument: <_new.value_> [place: 2]{end}\n")
            continue

        regedit_GetList = RegistryCp.items("reg")
        regedit_ListOfEntries = [entry[0] for entry in regedit_GetList]
        

        regedit_Name = regedit_Name.replace(" ", "")
        if regedit_Name not in regedit_ListOfEntries:
            print(f"  {red}Incorrect name of entry!{end}\n")
            continue

        if regedit_NewValue.replace(" ", "").lower() not in ("true", "false", "1", "0", "t", "f"):
            print(f"  {red}Value can be only{end} true {red}or{end} false{red}!{end}\n")
            continue

        if regedit_NewValue.replace(" ", "").lower() in ("true", "t", "1"):
            regedit_NewValue = "true"

        else:
            regedit_NewValue = "false"

        try:
            RegistryCp["reg"][regedit_Name] = regedit_NewValue
            with open(Registry_Loc, "w") as f:
                RegistryCp.write(f)

        except:        
            print(f"  {red}Cannot write new value.{end}\n")

    elif __Command__[0] == "regcopy":
        RegistryCp.read(Registry_Loc)
        RegistryEntries = RegistryCp.items("reg")

        ValuesList = []
        for i, entry in enumerate(RegistryEntries):
            ValuesList.append("1" if entry[1] == 'true' else "0")

        print(f"  {green}Your registry code:{end} {''.join(ValuesList)}", end="")
        if RegistryCp["reg"]["copyoutput"] == "true":
            pyperclip.copy(''.join(ValuesList))
            print(f"  {gray}(copied.){end}")

        print("\n")

    elif __Command__[0] == "regpaste":
        try:
            regpaste_Paste = __Command__[1]
            regpaste_Paste = regpaste_Paste.replace(" ", "")
        except:
            print(f"  {red}Missing argument: <_new.reg_>{end}\n")
            continue

        PastedList = list(regpaste_Paste)
        isElementError = False

        for element in PastedList:
            if element != "1":
                if element != "0":
                    print(f"  {red}Argument error: Code can handle only 1 and 0.{end}\n")
                    isElementError = True 
            if isElementError == True:
                break

        if isElementError == True:
                continue

        regpaste_GetList = RegistryCp.items("reg")
        regpaste_ListOfEntries = [entry[0] for entry in regpaste_GetList]
        
        if len(regpaste_ListOfEntries) != len(PastedList):
            print(f"  {red}Argument error: Entried code is too long or too short.{end}\n")
            continue 
        
        for i, element in enumerate(PastedList):
            RegistryCp["reg"][regpaste_ListOfEntries[i]] = 'true' if element == "1" else 'false'
            with open(Registry_Loc, "w") as f:
                RegistryCp.write(f)

    # Custom commands
    elif __Command__[0] in _CustomCommandsList_:
        RegistryCp.read(Registry_Loc)
        if RegistryCp["reg"]["enablecustomcommands"] == "false":
            print(f"  {red}Custom commands are disabled in registry.{end}")
            continue
        
        CommandsCp.read(Commands_Loc)
        try:
            exec(CommandsCp[__Command__[0]]["value"].replace("<br>", "\n"))
        except Exception as e:
            print(f"  {red}Cannot execute command.{end}")
            print(f"  {red}Exception:{end} {e}\n")

    elif __Command__[0] == "addcustomcmd":
        RegistryCp.read(Registry_Loc)
        if RegistryCp["reg"]["enablecustomcommands"] == "false":
            print(f"  {red}Custom commands are disabled in registry.{end}")
            continue

        try:
            addcmd_Name = __Command__[1]
            addcmd_Name = addcmd_Name.replace(" ","").lower()
        except:
            print(f"  {red}Missing argument: <_name_>{end}\n")
            continue

        CommandsCp[addcmd_Name] = {"value": "# This is your command. Use <br> to make new line."}
        
        with open(Commands_Loc, "w") as f:
            CommandsCp.write(f)

        os.system(f"notepad {Commands_Loc}")

    elif __Command__[0] == "opencustomcmd":
        RegistryCp.read(Registry_Loc)
        if RegistryCp["reg"]["enablecustomcommands"] == "false":
            print(f"  {red}Custom commands are disabled in registry.{end}")
            continue

        os.system(f"notepad {Commands_Loc}")

    elif __Command__[0] == "makecustom":
        RegistryCp.read(Registry_Loc)
        if RegistryCp["reg"]["enablecustomcommands"] == "false":
            print(f"  {red}Custom commands are disabled in registry.{end}")
            continue

        try:
            normalCode_Loc = __Command__[1].replace(" ","", 1)
            if not os.path.exists(normalCode_Loc):
                print(f"  {red}Path: \"{normalCode_Loc}\" does not exists!{end}\n")
                continue 

        except:
            print(f"  {red}Missing argument: <_code_>.{end}\n")
            continue
        
        FormattedCode = open(normalCode_Loc, "r").read().replace("\n", "<br>")
        print(FormattedCode)

        if RegistryCp["reg"]["copyoutput"] == "true":
            pyperclip.copy(FormattedCode)
            print(f"  {gray}(copied.){end}")

    elif __Command__[0] == "customlist":
        print("  Custom commands:")
        for command in _CustomCommandsList_:
            print(f"    • {command}")
    
        print("\n")


    else:
        ClearOneLine()
        print(f"({_Mode_}) {UserConfig.Name} {red}{UserConfig.Cursor}{end}{SpaceAfterCursor}{CommandContent}")

    
