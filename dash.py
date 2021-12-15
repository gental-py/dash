# Import packages
print("  [Info] Importing packages : ", end="")

try:
    import pyuac, sys, os, platform, getpass, socket, requests, getmac, pyperclip, configparser as cp, ctypes

except:
    print("Error : ",end="")
    from install_libaries import InstallRequiredPackages
    InstallRequiredPackages()
    __import__("os").system("cls")

    try:
        import pyuac, sys, os, platform, getpass, socket, requests, getmac, pyperclip, configparser as cp, ctypes
        print("Repaired : ",end="")
    
    except:
        print("Error")
        exit()

print("OK")


# System username
_OsUsername_ = getpass.getuser()


# Files
print("  [Info] Configuring configparser : ", end="")
VarsCP = cp.ConfigParser()
ConfigCP = cp.ConfigParser()
RegistryCP = cp.ConfigParser()
CommandsCP   = cp.ConfigParser()

Vars_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\vars.dash"
Config_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\config.dash"
Registry_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\reg.dash"
MainFolder_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\"
Commands_Path     = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\commands.dash"

print("OK")


# Check files health
print("  [Info] Checking files <", end="")
import check_files
check_files.check()
print("> : OK")


# Check if program is running on windows.
print("  [Info] Checking platform : ",end="")
if platform.system() != "Windows":
    print("  Hi user. Propably dash must run on Windows.")
    exit()
print("OK")


# Colors
print("  [Info] Setting up colors : ",end="")
if not sys.stdout.isatty():
    for _ in dir():
        if isinstance(_, str) and _[0] != "_":
            locals()[_] = ""
else:
    if platform.system() == "Windows":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        del kernel32
print("OK")


# Functions
def Cls():
    os.system("cls")
    print("\n")
def ClearOneLine():
    print("\033[A                                                             \033[A")
def ListToString(InList):
    DoneStr = ""
    for Element in InList:
        DoneStr += Element
    return DoneStr
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

# Configuration
def ReadUserConfig():
    ConfigCP.read(Config_Path, encoding='utf-8')
    _SepChar = ConfigCP["customization"]["sepchar"]
    _Cursor = ConfigCP["customization"]["cursor"]
    _Name = ConfigCP["customization"]["name"]
    _OsChar = ConfigCP["customization"]["oschar"]
    return (_Name, _Cursor, _SepChar, _OsChar)
def TurnColors():
    global end, red, gray, green, orange, blue
    RegistryCP.read(Registry_Path, encoding='utf-8')
    if RegistryCP["reg"]["enableColors"] == "false":
        end = ""
        red = ""
        gray = ""
        green = ""
        orange = ""
        blue = ""

# Format input
def FormatInput(UserInput):

    VarsCP.read(Vars_Path, encoding='utf-8')
    ConfigCP.read(Config_Path, encoding='utf-8')
    OsChar = ConfigCP["customization"]["oschar"]
    ListOfVariables = VarsCP.sections()

    if not UserInput.startswith(OsChar):
        FormatInput_sep = ReadUserConfig()[2]
        if FormatInput_sep == "_":
            FormatInput_sep = " "
    
        UserInputList = UserInput.split(FormatInput_sep)
        UserInputList[0] = UserInputList[0].replace(" ", "").lower()


        for i, argument in enumerate(UserInputList):
            argument = argument.replace(" ","").lower()
            argBef = argument
            for variable in ListOfVariables:
                argument = argument.replace("${"+variable+"}", VarsCP[variable]["value"])
                if argBef != argument:
                    UserInputList.pop(i)
                    UserInputList.insert(i, argument)

    else:
        UserInput = UserInput.replace(OsChar, "", 1)
        UserInputList = ["oscmd", UserInput]

        for i, argument in enumerate(UserInputList):
            argBef = argument
            for variable in ListOfVariables:
                argument = argument.replace("${"+variable+"}", VarsCP[variable]["value"])
                if argBef != argument:
                    UserInputList.pop(i)
                    UserInputList.insert(i, argument)


    return UserInputList


# showbootupinfo entry barrier
RegistryCP.read(Registry_Path)
if RegistryCP["reg"]["showBootupInfo"] == "true":
    os.system("pause")


#  Main loop
Cls()
while True:

    def HandleError(type, command, name, description, solution):
        _ErrorTrigger_ = False
        _ErrorContent_ = []
        _AdvancedOutputMode_ = False

        # Error Code
        error_Code = type + "." + command + "." + name

        # Define error output mode
        RegistryCP.read(Registry_Path)
        if RegistryCP["reg"]["advancedErrorOutput"] == "true":
            _AdvancedOutputMode_ = True
        else:
            _AdvancedOutputMode_ = False

        # Define error type as boolean
        if type.lower() == "soft":
            type = False

        elif type.lower() == "critical":
            type = True

        else:
            Cls()
            print(f"    {red}ErrorHandler: Unknown error type {type.lower()}.{end}")
            os.system("pause")

        # Error content as set
        _ErrorContent_ = (type, error_Code, command, name, description, solution)


        if _ErrorContent_[0] == False:
            if _AdvancedOutputMode_ == False:
                print(f"  {red}Error: {_ErrorContent_[4]}{end}")
                print(f"  {orange}Solution: {_ErrorContent_[5]}{end}\n")

            else:
                print(f"  {orange}===={end}{red} ERROR {end}{orange}===={end}")
                print(f"   {red}• {orange}Code:  {end}{red}<{_ErrorContent_[1]}>{end}")
                print(f"   {red}• {orange}Info:  {end}{red}{_ErrorContent_[3]}{end} {orange}in{end} {red}{_ErrorContent_[2]}{end}")
                print(f"   {red}• {orange}Sltn:  {end}{blue}{_ErrorContent_[5]}{end}\n")




    # Set mode
    if isAdmin() == True:
        _Mode_ = "root" 
    else:
        _Mode_ = "nrml"

    # Read user config
    VarsCP.read(Vars_Path, encoding='utf-8')
    ConfigCP.read(Config_Path, encoding='utf-8')
    RegistryCP.read(Registry_Path)
    CommandsCP.read(Commands_Path, encoding='utf-8')
    UserConfig_Read = ReadUserConfig()

    class UserConfig:
        Name = UserConfig_Read[0]
        Cursor = UserConfig_Read[1]
        Sepchar = UserConfig_Read[2]
        OsChar    = UserConfig_Read[3]

    _CustomCommandsList_ = CommandsCP.sections()

    # Colors
    end    =  "\033[0m"
    red    =  "\033[1;31m"
    gray   =  "\033[1;30m"
    blue   =  "\033[1;34m"
    green  =  "\033[1;32m"
    orange =  "\033[1;33m"
    TurnColors()

    # Main input
    __Command__ = input(f"({_Mode_}) {UserConfig.Name} {gray}{UserConfig.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}")
    CommandContent = __Command__
    __Command__ = FormatInput(__Command__)

    # Good command
    ClearOneLine()
    print(f"({_Mode_}) {UserConfig.Name} {green}{UserConfig.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}{CommandContent}")


    if __Command__[0]   == "exit":
        exit()

    elif __Command__[0] == "checkfiles":
        check_files.check()
        print("  Done.")

    elif __Command__[0] == "restart":
        os.system("py dash.py")
        Cls()
        exit()

    elif __Command__[0] == "cls":
        Cls()

    elif __Command__[0] == "argtest":
        for i, arg in enumerate(__Command__):
            print(f"  [{i}] = \"{arg}\"")
        print("\n")

    elif __Command__[0] == "devtest":
        # print("  •")
        HandleError("soft", __Command__[0], "AnError", "Data you entered is gugugaga", "To repair do megapapa")


    # Settings
    elif __Command__[0] == "mycfg":
        print(f"  Name      ==  \"{UserConfig.Name}\"")
        print(f"  Cursor    ==  \"{UserConfig.Cursor}\"")
        print(f"  Sepchar   ==  \"{UserConfig.Sepchar}\"")
        print(f"  Oschar    ==  \"{UserConfig.OsChar}\"\n")

    elif __Command__[0] == "setname":
        try:
            setname_NewName = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_name_>{end}\n")
            continue

        if setname_NewName.replace(" ", "") == "":
            print(f"  {red}Missing argument: <_name_>{end}\n")

        if RegistryCP["reg"]["checkArgLenght"] == "true":
            if len(setname_NewName) > 31:
                print(f"  {red}Argument error: <_name_> is too long. [MaxLen=30]{end}\n")
                continue
            
            if len(setname_NewName) == 0:
                print(f"  {red}Argument error: <_name_> is short. [MinLen=1]{end}\n")
                continue

        ConfigCP["customization"]["name"] = setname_NewName
        with open(Config_Path, "w", encoding='utf-8') as f:
            ConfigCP.write(f)

    elif __Command__[0] == "setcursor":
        try:
            setcursor_NewCursor = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_cursor_>{end}\n")
            continue

        if setcursor_NewCursor.replace(" ", "") == "":
            print(f"  {red}Missing argument: <_cursor_>{end}\n")

        if RegistryCP["reg"]["checkArgLenght"] == "true":
            if len(setcursor_NewCursor) > 6:
                print(f"  {red}Argument error: <_cursor_> is too long. MaxLen=5{end}\n")
                continue

            if len(setcursor_NewCursor) == 0:
                print(f"  {red}Argument error: <_cursor_> is short. [MinLen=1]{end}\n")
                continue

        ConfigCP["customization"]["cursor"] = setcursor_NewCursor
        with open(Config_Path, "w", encoding='utf-8') as f:
            ConfigCP.write(f)

    elif __Command__[0] == "setsepchar":
        try:
            setsepchar_NewChar = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_sepchar_>{end}\n")
            continue

        if RegistryCP["reg"]["checkArgLenght"] == "true":
            if len(setsepchar_NewChar) > 4:
                print(f"  {red}Argument error: <_sepchar_> is too long. [MaxLen=3]{end}\n")
                continue

            if len(setsepchar_NewChar) == 0:
                print(f"  {red}Argument error: <_sepchar_> cannot be blank{end}")

        ConfigCP["customization"]["sepchar"] = setsepchar_NewChar
        with open(Config_Path, "w", encoding='utf-8') as f:
            ConfigCP.write(f)

    elif __Command__[0] == "setoschar":
        try:
            setoschar_Char = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_oschar_>{end}")
            continue
        
        setoschar_Char = setoschar_Char.replace(" ", "")

        if RegistryCP["reg"]["checkArgLenght"] == "true":
            if len(setoschar_Char) > 1:
                print(f"  {red}Argument error: <_oschar_> is too long. [MaxLen=1]{end}\n")
                continue

        ConfigCP["customization"]["oschar"] = setoschar_Char
        with open(Config_Path, "w", encoding='utf-8') as f:
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

    elif __Command__[0] == "dnslkp":
        try:
            dnslkp_TargetIP = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_addres_>{end}\n")
            continue

        dnslkp_TargetIP = dnslkp_TargetIP.replace(" ", "")

        try:
            dnslkp_OutputIP = socket.gethostbyname(dnslkp_TargetIP)
            print(f"  IP {green}>{end} {dnslkp_OutputIP}", end="")

            RegistryCP.read(Registry_Path)
            if RegistryCP["reg"]["copyOutput"] == "true":
                pyperclip.copy(dnslkp_OutputIP)
                print(f"  {gray}(copied.){end}")

            print("\n")
        
        except:
            print(f"  {red}Cannot find out ip addres for: {end}{dnslkp_TargetIP}\n")

    elif __Command__[0] == "revdnslkp":
        try:
            revdnslkp_TargetIP = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_addres_>{end}\n")
            continue

        revdnslkp_TargetIP = revdnslkp_TargetIP.replace(" ", "")

        try:
            revdnslkp_OutputIP = socket.gethostbyaddr(revdnslkp_TargetIP)
            print(f"  IP {green}>{end} {revdnslkp_OutputIP[0]}", end="")

            RegistryCP.read(Registry_Path)
            if RegistryCP["reg"]["copyOutput"] == "true":
                pyperclip.copy(revdnslkp_OutputIP[0])
                print(f"  {gray}(copied.){end}")
        
        except:
            print(f"  {red}Cannot find addres for: {end}{revdnslkp_TargetIP}\n")
        print("")

    elif __Command__[0] == "ipgeoinfo":
        try:
            ipgeoinfo_TargetIP = __Command__[1]
            ipgeoinfo_TargetIP = ipgeoinfo_TargetIP.replace(" ","")
        except:
            print(f"  {red}Missing argument: <_ip_>{end}\n")
            continue

        try:
            ipinfo_REQ = requests.get(f"http://ip-api.com/json/{ipgeoinfo_TargetIP}")
            ipinfo_JSON = ipinfo_REQ.json()

            if ipgeoinfo_TargetIP.replace(" ","") == "": ipgeoinfo_TargetIP = "Localhost"

            print(f"  Country:  {ipinfo_JSON['country']}     [{ipinfo_JSON['countryCode']}]")
            print(f"  City   :  {ipinfo_JSON['city']}      [{ipinfo_JSON['zip']}]\n")

        except:
            print(f"  {red}Error: Cannot load information about ip:{end} {ipgeoinfo_TargetIP}\n")


    # Registry
    elif __Command__[0] == "dregshow":
        RegistryCP.read(Registry_Path)
        RegistryEntries = RegistryCP.items("reg")

        print("  ==== REGSHOW ====\n")
        for i, entry in enumerate(RegistryEntries):
            print(f"  [{i+1}] |  {green+'T' if entry[1] == 'true' else red+'F'}{end} {entry[0]}")

        print("\n")

    elif __Command__[0] == "dregedit":

        try:
            dregedit_EntryName = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_entry.name_> [place: 1]{end}\n")
            continue

        try:
            dregedit_NewValue = __Command__[2]
        except:
            print(f"  {red}Missing argument: <_new.value_> [place: 2]{end}\n")
            continue

        dregedit_StableEntriesList = RegistryCP.items("reg")
        dregedit_ListOfEntries = [entry[0] for entry in dregedit_StableEntriesList]
        
        dregedit_EntryName = dregedit_EntryName.replace(" ", "")
        if dregedit_EntryName not in dregedit_ListOfEntries:
            print(f"  {red}Incorrect name of entry!{end}\n")
            continue

        if dregedit_NewValue.replace(" ", "").lower() not in ("true", "false", "1", "0", "t", "f"):
            print(f"  {red}Value can be only{end} true {red}or{end} false{red}!{end}\n")
            continue

        if dregedit_NewValue.replace(" ", "").lower() in ("true", "t", "1"):
            dregedit_NewValue = "true"

        else:
            dregedit_NewValue = "false"

        try:
            RegistryCP["reg"][dregedit_EntryName] = dregedit_NewValue
            with open(Registry_Path, "w") as f:
                RegistryCP.write(f)

        except:        
            print(f"  {red}Cannot write new value.{end}\n")

    elif __Command__[0] == "dregcopy":
        RegistryCP.read(Registry_Path)
        dregcopy_StableEntriesList = RegistryCP.items("reg")

        dregedit_OutputList = []
        for i, entry in enumerate(dregcopy_StableEntriesList):
            dregedit_OutputList.append("1" if entry[1] == 'true' else "0")

        print(f"  {green}Your registry code:{end} {''.join(dregedit_OutputList)}", end="")
        if RegistryCP["reg"]["copyoutput"] == "true":
            pyperclip.copy(''.join(dregedit_OutputList))
            print(f"  {gray}(copied.){end}")

        print("\n")

    elif __Command__[0] == "dregpaste":
        try:
            dregpaste_Code = __Command__[1]
            dregpaste_Code = dregpaste_Code.replace(" ", "")
        except:
            print(f"  {red}Missing argument: <_new.reg_>{end}\n")
            continue

        dregpaste_CodeList = list(dregpaste_Code)
        dregpaste_ElementErrorTrigger = False

        for element in dregpaste_CodeList:
            if element != "1":
                if element != "0":
                    print(f"  {red}Argument error: Code can handle only 1 and 0.{end}\n")
                    dregpaste_ElementErrorTrigger = True 
            if dregpaste_ElementErrorTrigger == True:
                break

        if dregpaste_ElementErrorTrigger == True:
                continue

        dregpaste_StableEntriesList = RegistryCP.items("reg")
        dregpaste_ListOfEntries = [entry[0] for entry in dregpaste_StableEntriesList]
        
        if len(dregpaste_ListOfEntries) != len(dregpaste_CodeList):
            print(f"  {red}Argument error: Entried code is too long or too short.{end}\n")
            continue 
        
        for i, element in enumerate(dregpaste_CodeList):
            RegistryCP["reg"][dregpaste_ListOfEntries[i]] = 'true' if element == "1" else 'false'
            with open(Registry_Path, "w") as f:
                RegistryCP.write(f)

    elif __Command__[0] == "dregreset":
        
        print(f"  {orange}Warning: Registry will be setted back to deafult. Do you really want to continue?{end}")
        dregreset_Confirmation = input('  "confirm" to continue:  ')

        if dregreset_Confirmation.lower().replace(" ", "") == "confirm":
            open(Registry_Path, "w+").close()
            Cls()
            os.system("py dash.py")
            exit()

        print("\n")


    # Custom commands
    elif __Command__[0] in _CustomCommandsList_:
        RegistryCP.read(Registry_Path)
        if RegistryCP["reg"]["enablecustomcommands"] == "false":
            print(f"  {red}Custom commands are disabled in registry.{end}\n")
            continue

        CommandsCP.read(Commands_Path, encoding='utf-8')
        try:
            exec(CommandsCP[__Command__[0]]["value"].replace("<br>", "\n"))
        except Exception as e:
            print(f"  {red}Cannot execute command.{end}")
            print(f"  {red}Exception:{end} {e}\n")

    elif __Command__[0] == "addcustomcmd":
        RegistryCP.read(Registry_Path)
        if RegistryCP["reg"]["enablecustomcommands"] == "false":
            print(f"  {red}Custom commands are disabled in registry.{end}\n")
            continue

        try:
            addcmd_Name = __Command__[1]
            addcmd_Name = addcmd_Name.replace(" ","").lower()
        except:
            print(f"  {red}Missing argument: <_name_>{end}\n")
            continue

        if addcmd_Name.replace(" ","") == "":
            print(f"  {red}Command name cannot be blank!{end}")
            continue

        CommandsCP[addcmd_Name] = {"value": "\"\"\" This is your command. Use <br> to make new line. To use arguments, type: '__Command__[x]' where x means place of argument. \"\"\""}
        
        with open(Commands_Path, "w", encoding='utf-8') as f:
            CommandsCP.write(f)

        os.system(f"notepad {Commands_Path}")

    elif __Command__[0] == "opencustomcmd":
        RegistryCP.read(Registry_Path)
        if RegistryCP["reg"]["enablecustomcommands"] == "false":
            print(f"  {red}Custom commands are disabled in registry.{end}\n")
            continue

        os.system(f"notepad {Commands_Path}")

    elif __Command__[0] == "convertcustom":
        RegistryCP.read(Registry_Path)
        if RegistryCP["reg"]["enablecustomcommands"] == "false":
            print(f"  {red}Custom commands are disabled in registry.{end}\n")
            continue

        try:
            convertcustom_Mode = __Command__[1]
            convertcustom_Mode = convertcustom_Mode.replace(" ","").lower()

        except:
            print(f"  {red}Missing argument: <_mode_>  [Place: 1].{end} Possible values: [file/f] , [text/t]\n")
            continue

        if convertcustom_Mode not in ("text", "t", "file", "f"):
            print(f"  {red}Argument error: <_mode_> [Place: 1].{end} Posible values: [file/f] , [text/t]\n")
            continue
        
        if convertcustom_Mode in ("file", "f"):
            try:
                convertcustom_ModeF_CodePath = __Command__[2].replace(" ","", 1)
                if not os.path.exists(convertcustom_ModeF_CodePath):
                    print(f"  {red}Path: \"{convertcustom_ModeF_CodePath}\" does not exists!{end}\n")
                    continue 

            except:
                print(f"  {red}Missing argument: <_code_>. [Place: 2]{end}\n")
                continue
            
            convertcustom_FormattedCode = open(convertcustom_ModeF_CodePath, "r", encoding='utf-8').read().replace("\n", "<br>")
            print(convertcustom_FormattedCode)

            if RegistryCP["reg"]["copyOutput"] == "true":
                pyperclip.copy(convertcustom_FormattedCode)
                print(f"  {gray}(copied.){end}\n")

        else:
            try:
                print("\n")

                convertcustom_ModeT_LinesList = []
                convertcustom_ModeT_LinesCounter = 1
                while True:
                    convertcustom_ModeT_CurrentLine = input(f"{convertcustom_ModeT_LinesCounter}  ")
                    if convertcustom_ModeT_CurrentLine == "<stop>":
                        break
                    else:
                        convertcustom_ModeT_LinesList.append(convertcustom_ModeT_CurrentLine)

                    convertcustom_ModeT_LinesCounter += 1

                convertcustom_ModeT_ReadyCode = '<br>'.join(convertcustom_ModeT_LinesList)
                print(f"  Code: {convertcustom_ModeT_ReadyCode}")

                if RegistryCP["reg"]["copyOutput"] == "true":
                    pyperclip.copy(convertcustom_ModeT_ReadyCode)
                    print(f"  {gray}(copied.){end}\n")

            except:
                print(f"  {red}Missing argument: <_code_>. [Place: 2]{end}\n")
                continue

    elif __Command__[0] == "customlist":
        print("  Custom commands:")
        for command in _CustomCommandsList_:
            print(f"    • {command}")
    
        print("\n")


    # Variables
    elif __Command__[0] == "vars":
        VarsCP.read(Vars_Path, encoding='utf-8')
        vars_ListOfVariables = VarsCP.sections()
        for name in vars_ListOfVariables:
            print(f"  {name} = \"{VarsCP[name]['value']}\"")

        print("\n")
        
    elif __Command__[0] == "varadd":
        try:
            varadd_Name = __Command__[1]
            varadd_Name = varadd_Name.replace(" ","").lower()
            
        except:
            print(f"  {red}Missing argument: <_name_>{end}\n")
            continue  

        varadd_ListOfVariables = VarsCP.sections()
        if varadd_Name in varadd_ListOfVariables:
            print(f"  {red}Variable named {varadd_Name} already exists!{end}\n")
            continue

        try:
            varadd_Value = __Command__[2]
            varadd_Value = varadd_Value.replace(" ", "", 1)

        except:
            print(f"  {red}Missing argument: <_value_>{end}\n")
            continue

        VarsCP[varadd_Name] = {"value": varadd_Value}
        with open(Vars_Path, "w", encoding='utf-8') as f:
            VarsCP.write(f)

    elif __Command__[0] == "remvar":
        try:
            remvar_Name = __Command__[1]
            remvar_Name = remvar_Name.replace(" ","").lower()

        except:
            print(f"  {red}Missing argument: <_name_>{end}\n")
            continue  

        VarsCP.read(Vars_Path, encoding='utf-8')
        remvar_ListOfVariables = VarsCP.sections()
        remvar_currentVars = [] 
        for varname in remvar_ListOfVariables:
            remvar_currentVars.append(varname.replace(" ","").lower())
            
        if remvar_Name not in remvar_currentVars:
            print(f"  {red}Variable named {remvar_Name} does not exists!{end}\n")
            continue

        try:
            VarsCP.remove_section(remvar_Name)    
            with open(Vars_Path, "w", encoding='utf-8') as f:
                VarsCP.write(f)

        except:
            print(f"  {red}Cannot delete variable.{end}")

    elif __Command__[0] == "varset":
        try:
            varset_Name = __Command__[1]
            varset_Name = varset_Name.replace(" ","").lower()

        except:
            print(f"  {red}Missing argument: <_name_> [Place: 1]{end}\n")
            continue  

        VarsCP.read(Vars_Path, encoding='utf-8')
        varset_ListOfVariables = VarsCP.sections()
        varset_currentVars = [] 
        for varname in varset_ListOfVariables:
            varset_currentVars.append(varname.replace(" ","").lower())
            
        if varset_Name not in varset_currentVars:
            print(f"  {red}Variable named {varset_Name} does not exists!{end}\n")
            continue

        try:
            varset_NewValue = __Command__[2]

        except:
            print(f"  {red}Missing argument: <_new.value_> [Place: 2]{end}\n")
            continue

        try:
            VarsCP[varset_Name]["value"] = varset_NewValue
            with open(Vars_Path, "w", encoding='utf-8') as f:
                VarsCP.write(f)

        except:
            print(f"  {red}Cannot change value.{end}")


    # Other
    elif __Command__[0] == "oscmd":
        ClearOneLine()
        print(f"({_Mode_}) {UserConfig.Name} {blue}{UserConfig.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}{CommandContent}")

        try:
            oscmd_Command = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_command_>{end}")
            continue

        try:
            os.system(oscmd_Command)
        except Exception as exc:
            print(f"  {red}Unexcpeted error: {exc}{end}")

    elif __Command__[0] == "root":
        try:
            pyuac.runAsAdmin()
        except:
            print(f"  {red}Cannot run Dash with administrator permissions.{end}")

    elif __Command__[0] == "viewf":
        try:
            viewf_file_Path = __Command__[1]
        except:
            print(f"  {red}Missing argument: <_file_>{end}")
            continue

        if not os.path.exists(viewf_file_Path):
            if not os.path.exists(viewf_file_Path.replace(" ","")):
                print(f"  {red}File does not exists{end}")
                continue

            else:
                viewf_file_Path = viewf_file_Path.replace(" ","")

        try:
            viewf_Open = open(viewf_file_Path, "r", encoding='utf-8')
            viewf_Lines = viewf_Open.readlines()
            print(f"{gray}\n  File: {os.path.basename(viewf_file_Path)}{end}\n")
            for counter, line in enumerate(viewf_Lines):
                # Convert line
                line = line.replace("\n","")
                line = line.replace("=", f"{blue}={end}")
                print(f"{orange}{'   ' if counter+1 < 10 else '  '}{counter+1}{end}  {gray}│{end}  {line} ") 
            print("\n")

        except:
            print(f"  {red}Cannot read file.{end}")
        

    else:
        ClearOneLine()
        print(f"({_Mode_}) {UserConfig.Name} {red}{UserConfig.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}{CommandContent}")

