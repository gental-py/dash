_Version_ = 7

try:
    # Import packages
    print("  [Info] Importing packages: ", end="")
    try:
        import bcrypt, sys, os, platform, getpass, socket, requests, getmac, pyperclip, configparser as cp, ctypes

    except:
        print("Error : ",end="")
        from install_libaries import InstallRequiredPackages
        InstallRequiredPackages()
        __import__("os").system("cls")

        try:
            import bcrypt, sys, os, platform, getpass, socket, requests, getmac, pyperclip, configparser as cp, ctypes
            print("Repaired : ",end="")
        
        except:
            print("Error")
            exit()
    print("OK")


    # System username
    _OsUsername_ = getpass.getuser()


    # Check for updates
    print("  [Info] Checking version  : ",end="")
    detectedUpdate  = False
    git_VersionFile = "https://raw.githubusercontent.com/GentalYT/dash/main/version"
    git_Request     = requests.get(git_VersionFile).text.replace("\n", "")

    if _Version_ != git_Request:
        try:
            git_Request = int(git_Request)  

        except:
            print("VersionFile.NonIntValue",end="")

        if git_Request > _Version_:
            detectedUpdate = True  
            print("Detected Update!")
    print("OK")


    # Files
    print("  [Info] Configuring configparser : ", end="")
    VarsCP = cp.ConfigParser()
    ConfigCP = cp.ConfigParser()
    RegistryCP = cp.ConfigParser()
    CommandsCP   = cp.ConfigParser()

    Registry_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\reg.dash"
    MainFolder_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\"
    print("OK")


    # Check files health
    print("  [Info] Checking files <", end="")
    import files_operations
    files_operations.check()
    print("> : OK")


    # Check root account
    print("  [Info] Checking root account : ",end="")
    import accounts
    try:
        accounts.UserInfo("root")
    except:
        accounts.setup_root()
    try:
        accounts.login("root", "bootup_test")
    except:
        accounts.setup_root()
    print("OK")


    # Check if program is running on windows.
    print("  [Info] Checking platform : ",end="")
    if platform.system() != "Windows": print("  Hi user. Propably dash must run on Windows."), exit() 
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
    def Restart():
        DashPath = os.getcwd()+"\\dash.py"
        try:
            os.system(f"py {DashPath}")
        except Exception as e:
            print(f"Error: cannot rerun dash. {e}")

    # Configuration
    def ReadUserAccount(name):
        __UserAccountPath = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{name}\\"
        ConfigCP.read(__UserAccountPath+"config.dash", encoding='utf-8')
        _SepChar = ConfigCP["customization"]["sepchar"]
        _Name    = _Login_Name
        _Cursor = ConfigCP["customization"]["cursor"]
        _OsChar = ConfigCP["customization"]["oschar"]

        import accounts
        _Permissions = accounts.UserInfo(_Login_Name)[1]
        if _Permissions.replace(" ","").replace("\n","") == "u":
            _Permissions = "user"
        elif _Permissions.replace(" ","").replace("\n","") == "r":
            _Permissions = "root"
        else:
            _Permissions = "user"
       
        return (_Name, _Cursor, _SepChar, _OsChar, _Permissions, __UserAccountPath)
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
            FormatInput_sep = ReadUserAccount(_Login_Name)[2]
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
    def RemoveStartSpaces(text):
        listed = list(text)
        for i, char in enumerate(listed):
            if char == " ":
                listed.pop(i)
        
        for i, char in enumerate(listed):
            if i != 0:
                if char == " ":
                    listed.pop(-i)

        return ListToString(listed)


    # showbootupinfo entry barrier
    RegistryCP.read(Registry_Path)
    if RegistryCP["reg"]["showBootupInfo"] == "true":
        os.system("pause")


    # Login 
    while True:
        os.system("cls")
        print("  Login to your account.")
        _Login_Name = input(f"  Name : ")
        _Login_Password = getpass.getpass(f"  Password : ") 
        try:
            import accounts

        except:
            print(f"  {red}Critical error: Cannot import accounts module. Including autorepair system.{end}")
            try:
                import update_code
                print("  [ ok ]    : Imported <update_code>.")
                Restart()

            except:
                print("  [ error ] : <update_code> not found.")
                print("  Cannot repair error automaticly. You have to repair it by yourself. (mod.acc._notfound_)")
                exit()

        _Login_Status = accounts.login(_Login_Name, _Login_Password)
        
        if _Login_Status == True:
            print(f"  Welcome, {_Login_Name}")
            break


        else:
            print(f"  {_Login_Status}")
            os.system("pause")


    #  Main loop
    Cls()
    while True:

        # If update detected
        if detectedUpdate == True:
            detectedUpdate = False
            print(f"\n\n  Dash have detected update! [{git_Request}]")

            if RegistryCP["reg"]["autoupdate"] == "true":
                print("  Autoupdate is true, installing update.")
                import update_code
                exit()

            else:
                update_Ask = input("  Do you want to automaticly install update? [Y/n] >").replace(" ","").lower()
                while update_Ask not in ("y", "n"):
                    update_Ask = input("  [Y/n] >").replace(" ","").lower()

                if update_Ask == "y":
                    import update_code
                    exit()

        def HandleError(type, command, name, description, solution):
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
                    print(f"   {red}• {orange}Info:  {end}{red}{_ErrorContent_[4]}{end}")
                    print(f"   {red}• {orange}Sltn:  {end}{blue}{_ErrorContent_[5]}{end}\n")
            else:
                Cls()
                print(f"  {orange}===={end}{red} CRITICAL ERROR {end}{orange}===={end}")
                print(f"   {red}• {orange}Code:  {end}{red}<{_ErrorContent_[1]}>{end}")
                print(f"   {red}• {orange}Info:  {end}{red}{_ErrorContent_[4]}{end}")
                print(f"   {red}• {orange}Sltn:  {end}{blue}{_ErrorContent_[5]}{end}\n")

                import critical_mode
                critical_mode.CriticalMode(_ErrorContent_[1])
                exit()

        # Set paths variables
        Vars_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{_Login_Name}\\vars.dash"
        Config_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{_Login_Name}\\config.dash"
        Commands_Path  = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{_Login_Name}\\commands.dash"
    
        # Read user config
        UserAccount_Read = ReadUserAccount(_Login_Name)
        __UserAccountPath = UserAccount_Read[-1]

        VarsCP.read(__UserAccountPath+"vars.dash", encoding='utf-8')
        ConfigCP.read(__UserAccountPath+"config.dash", encoding='utf-8')
        CommandsCP.read(__UserAccountPath+"commands.dash", encoding='utf-8')
        RegistryCP.read(Registry_Path)

        _CustomCommandsList_ = CommandsCP.sections()

        class UserAccount:
            Name = UserAccount_Read[0]
            Cursor = UserAccount_Read[1]
            Sepchar = UserAccount_Read[2]
            OsChar   = UserAccount_Read[3]
            Permissions = UserAccount_Read[4]

        # Colors
        end    =  "\033[0m"
        red    =  "\033[1;31m"
        gray   =  "\033[1;30m"
        blue   =  "\033[1;34m"
        green  =  "\033[1;32m"
        orange =  "\033[1;33m"
        TurnColors()

        # Mode
        _Mode_ = UserAccount.Permissions

        # Main input     
        __Command__ = input(f"[{_Mode_}] {UserAccount.Name} {gray}{UserAccount.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}")
        CommandContent = __Command__
        __Command__ = FormatInput(__Command__)

        # Good command
        ClearOneLine()
        print(f"[{_Mode_}] {UserAccount.Name} {green}{UserAccount.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}{CommandContent}")
        os.system(f"title {__Command__[0]}")


        if __Command__[0]   == "exit":
            exit()

        elif __Command__[0] == "restart":
            Restart()
            exit()

        elif __Command__[0] == "cls":
            Cls()

        elif __Command__[0] == "devtest":
            print("  •")


        # Settings
        elif __Command__[0] == "mycfg":
            try:
                print(f"\n  Current configuration{gray}:{end} \n")
                print(f"    Name    = {gray}\"{end}{UserAccount.Name}{gray}\"{end}")
                print(f"    Cursor  = {gray}\"{end}{UserAccount.Cursor}{gray}\"{end}")
                print(f"    Sepchar = {gray}\"{end}{UserAccount.Sepchar}{gray}\"{end}")
                print(f"    Oschar  = {gray}\"{end}{UserAccount.OsChar}{gray}\"{end}\n")

            except Exception as exc:
                HandleError("critical", __Command__[0], exc, "Cannot read user configuration", "None")

        elif __Command__[0] == "set.cursor":
            try:
                setcursor_NewCursor = RemoveStartSpaces(__Command__[1])
                if setcursor_NewCursor == "dot":
                    setcursor_NewCursor = "•"
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <cursor> not found.", f"After command, type sepchar (current: \"{UserAccount.Sepchar}\") and your new cursor")
                continue

            if setcursor_NewCursor.replace(" ", "") == "":
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <cursor> not found.", f"After command, type sepchar (current: \"{UserAccount.Sepchar}\") and your new cursor")
                continue

            if RegistryCP["reg"]["checkArgLenght"] == "true":
                if len(setcursor_NewCursor) > 6:
                    HandleError("soft", __Command__[0], "ArgumentLenghtError", "Argument: <cursor> cannot be longer than 5 characters.", "Type shorter cursor")
                    continue
            
            try:
                ConfigCP["customization"]["cursor"] = setcursor_NewCursor
                with open(Config_Path, "w", encoding='utf-8') as f:
                    ConfigCP.write(f)
            except:
                HandleError("critical", __Command__[0], "FileError", "Cannot write to file.", "None")
                continue

        elif __Command__[0] == "set.sepchar":
            try:
                setsepchar_NewChar = __Command__[1].replace(" ","")
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <sepchar> not found", f"After command, type sepchar (current: \"{UserAccount.Sepchar}\") and your new sepchar")
                continue

            if RegistryCP["reg"]["checkArgLenght"] == "true":
                if len(setsepchar_NewChar) > 4:
                    HandleError("soft", __Command__[0], "ArgumentLenghtError", "Argument: <sepchar> is too long.", "Type shorter sepchar.")
                    continue
            
            if "." in setsepchar_NewChar:
                print(f"  {orange}Sepchar cannot include dot (\".\") becouse of some commands names conflict.")
                continue

            try:
                ConfigCP["customization"]["sepchar"] = setsepchar_NewChar
                with open(Config_Path, "w", encoding='utf-8') as f:
                    ConfigCP.write(f)
            except:
                HandleError("critical", __Command__[0], "FileError", "Cannot write to file.", "None")

        elif __Command__[0] == "set.oschar":
            try:
                setoschar_Char = RemoveStartSpaces(__Command__[1])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <setoschar> not found", f"After command, type sepchar (current: \"{UserAccount.Sepchar}\") and your new setoschar")
                continue
            
            setoschar_Char = setoschar_Char.replace(" ", "")

            if RegistryCP["reg"]["checkArgLenght"] == "true":
                if len(setoschar_Char) > 1:
                    HandleError("soft", __Command__[0], "ArgumentLenghtError", "Argument: <setoschar> is too long.", "Type shorter setoschar.")
                    continue
            
            try:
                ConfigCP["customization"]["oschar"] = setoschar_Char
                with open(Config_Path, "w", encoding='utf-8') as f:
                    ConfigCP.write(f)
            except:
                HandleError("critical", __Command__[0], "FileError", "Cannot write to file.", "None")


        # Network
        elif __Command__[0] == "netinfo":
            try:
                netinfo_PrivateIP = socket.gethostbyname(socket.gethostname())
                netinfo_PublicIP  = requests.get('https://api.ipify.org').text
                netinfo_PcName    = socket.gethostname()
                netinfo_MacAddr   = getmac.get_mac_address()

                print(f" - IP:\n  Public  {green}>{end} {netinfo_PublicIP}\n  Private {green}>{end} {netinfo_PrivateIP}\n  Mac     {green}>{end} {netinfo_MacAddr}\n")
                print(f" - NAME:\n  This pc {green}>{end} {netinfo_PcName}\n")

            except Exception as exc:
                HandleError("soft", __Command__[0], "FetchingInfoError", f"Cannot load informations: <{exc}>", "None")

        elif __Command__[0] == "dnslkp":
            try:
                dnslkp_TargetIP = __Command__[1]
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <target> not found", f"After command, type sepchar (current: \"{UserAccount.Sepchar}\") and target ip.")
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
                HandleError("soft", __Command__[0], "FetchingInfoError", "Cannot load informations.", "None")

        elif __Command__[0] == "revdnslkp":
            try:
                revdnslkp_TargetIP = __Command__[1]
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <target> not found", f"After command, type sepchar (current: \"{UserAccount.Sepchar}\") and target ip.")
                continue

            revdnslkp_TargetIP = revdnslkp_TargetIP.replace(" ", "")

            try:
                revdnslkp_OutputIP = socket.gethostbyaddr(revdnslkp_TargetIP)
                print(f"  IP {green}>{end} {revdnslkp_OutputIP[0]}", end="")

                RegistryCP.read(Registry_Path)
                if RegistryCP["reg"]["copyOutput"] == "true":
                    pyperclip.copy(revdnslkp_OutputIP[0])
                    print(f"  {gray}(copied.)\n{end}")
            
            except:
                HandleError("soft", __Command__[0], "FetchingInfoError", "Cannot load informations.", "None")

        elif __Command__[0] == "ipgeoinfo":
            try:
                ipgeoinfo_TargetIP = __Command__[1]
                ipgeoinfo_TargetIP = ipgeoinfo_TargetIP.replace(" ","")

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <ip> not found.", "Type argument <ip>.")
                continue

            try:
                ipinfo_REQ = requests.get(f"http://ip-api.com/json/{ipgeoinfo_TargetIP}")
                ipinfo_JSON = ipinfo_REQ.json()

                if ipgeoinfo_TargetIP.replace(" ","") == "": ipgeoinfo_TargetIP = "Localhost"

                print(f"  Country:  {ipinfo_JSON['country']}  [{ipinfo_JSON['countryCode']}]")
                print(f"  City   :  {ipinfo_JSON['city']}  [{ipinfo_JSON['zip']}]\n")

            except:
                HandleError("soft", __Command__[0], "FetchingInfoError", "Cannot load informations.", "None")


        # Registry
        elif __Command__[0] == "dreg.show":
            try:
                RegistryCP.read(Registry_Path)
                RegistryEntries = RegistryCP.items("reg")

                print("\n  ==== REGSHOW ====\n")
                for i, entry in enumerate(RegistryEntries):
                    print(f"  [{i+1}] {gray}|{end} {green+'T' if entry[1] == 'true' else red+'F'}{end} {gray}|{end} {entry[0]}")

                print("\n")

            except Exception as exc:
                HandleError("critical", __Command__[0], "LoadingRegInfoError", f"Exception: {exc}", "None")

        elif __Command__[0] == "dreg.edit":

            if _Mode_ != "root":
                HandleError("soft", __Command__[0], "PermissionsError", "Only [root] can edit registry.", "Execute command with root permisions.")
                continue

            try:
                dregedit_EntryName = __Command__[1].replace(" ","")
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <entry.name> not found.", "Type argument: <entry.name>")
                continue

            try:
                dregedit_NewValue = RemoveStartSpaces(__Command__[2])

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <entry.value> not found.", "Type argument: <entry.value>")
                continue
            
            dregedit_EntryName = dregedit_EntryName.replace(" ", "")
            dregedit_StableEntriesList = RegistryCP.items("reg")
            dregedit_ListOfEntries = [entry[0] for entry in dregedit_StableEntriesList]
            dregedit_EntriesIndexes = {}

            for i, entry in enumerate(dregedit_ListOfEntries):
                dregedit_EntriesIndexes[str(i+1)] = entry

            # Check if putted entryname as index
            try:
                dregedit_EntryName = int(dregedit_EntryName)
                if dregedit_EntryName not in range(1, len(dregedit_StableEntriesList)):
                        HandleError("soft", __Command__[0], "EntryNameIndexError", "Given entry index is incorrect.", "Enter correct entry index or name.")
                        continue

                for num in range(1, len(dregedit_StableEntriesList)):
                    if dregedit_EntryName == num:
                        dregedit_EntryName = dregedit_StableEntriesList[num-1][0]
                        break
            except:
                pass
     
            if dregedit_EntryName not in dregedit_ListOfEntries:
                HandleError("soft", __Command__[0], "EntryNotFound", "Argument: <entry.name> don't fit.", "Type correct argument: <entry.name>")
                continue

            if dregedit_NewValue.replace(" ", "").lower() not in ("true", "false", "1", "0", "t", "f"):
                HandleError("soft", __Command__[0], "EntryValueError", "Argument: <entry.value> is incorrect.", "If you want to turn on, type: (t/true/1) otherwise: (f/false/0)")
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
                HandleError("critical", __Command__[0], "FileError", "Cannot write to file.", "None")

        elif __Command__[0] == "dreg.copy":
            try:
                RegistryCP.read(Registry_Path)
                dregcopy_StableEntriesList = RegistryCP.items("reg")

                dregedit_OutputList = []
                for i, entry in enumerate(dregcopy_StableEntriesList):
                    dregedit_OutputList.append("1" if entry[1] == 'true' else "0")

                print(f"  {blue}Your registry code:{end} {orange}{''.join(dregedit_OutputList)}{end}", end="")
                if RegistryCP["reg"]["copyoutput"] == "true":
                    pyperclip.copy(''.join(dregedit_OutputList))
                    print(f"  {gray}(copied.){end}")

        
            except:
                HandleError("critical", __Command__[0], "LoadingRegInfoError")

        elif __Command__[0] == "dreg.paste":
            try:
                dregpaste_Code = __Command__[1]
                dregpaste_Code = dregpaste_Code.replace(" ", "")
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <code> not found.", "Type argument: <code>")
                continue

            dregpaste_CodeList = list(dregpaste_Code)
            dregpaste_ElementErrorTrigger = False

            for element in dregpaste_CodeList:
                if element != "1":
                    if element != "0":
                        HandleError("soft", __Command__[0], "RegCodeValueError", f"Element: {element} is not 0 or 1", "None")
                        dregpaste_ElementErrorTrigger = True 
                if dregpaste_ElementErrorTrigger == True:
                    break

            if dregpaste_ElementErrorTrigger == True:
                continue

            dregpaste_StableEntriesList = RegistryCP.items("reg")
            dregpaste_ListOfEntries = [entry[0] for entry in dregpaste_StableEntriesList]
            
            if len(dregpaste_ListOfEntries) != len(dregpaste_CodeList):
                HandleError("soft", __Command__[0], "ArgumentLenghtError", "Typed code is too long or too short.", "Check lenght of code.")
                continue 
            
            try:
                for i, element in enumerate(dregpaste_CodeList):
                    RegistryCP["reg"][dregpaste_ListOfEntries[i]] = 'true' if element == "1" else 'false'
                    with open(Registry_Path, "w") as f:
                        RegistryCP.write(f)
            except:
                HandleError("critical", __Command__[0], "FileError", "Cannot write to file.", "None")

        elif __Command__[0] == "dreg.reset":

            if _Mode_ != "root":
                HandleError("soft", __Command__[0], "PermissionsError", "Only [root] can edit registry.", "Execute command with root permisions.")
                continue

            
            print(f"  {orange}Warning: Registry will be set back to deafult. Do you really want to continue?{end}")
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

        elif __Command__[0] == "cstm.add":
            RegistryCP.read(Registry_Path)
            if RegistryCP["reg"]["enablecustomcommands"] == "false":
                print(f"  {red}Custom commands are disabled in registry.{end}\n")
                continue

            try:
                addcmd_Name = __Command__[1]
                addcmd_Name = RemoveStartSpaces(addcmd_Name).lower()

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", "Type argument: <name>.")
                continue

            if addcmd_Name.replace(" ","") == "":
                HandleError("soft", __Command__[0], "ArgumentLenghtError", "Argument: <name> cannot be blank.", "Type longer argument: <name>.")
                continue

            CommandsCP[addcmd_Name] = {"value": "\"\"\" This is your command. Use <br> to make new line. To use arguments, type: '__Command__[x]' where x means place of argument. \"\"\""}
            
            try:
                with open(Commands_Path, "w", encoding='utf-8') as f:
                    CommandsCP.write(f)
            except:
                HandleError("critical", __Command__[0], "FileError", "Cannot write to file.", "None")

            os.system(f"notepad {Commands_Path}")

        elif __Command__[0] == "cstm.open":
            RegistryCP.read(Registry_Path)
            if RegistryCP["reg"]["enablecustomcommands"] == "false":
                print(f"  {red}Custom commands are disabled in registry.{end}\n")
                continue

            os.system(f"notepad {Commands_Path}")

        elif __Command__[0] == "cstm.convert":
            RegistryCP.read(Registry_Path)
            if RegistryCP["reg"]["enablecustomcommands"] == "false":
                print(f"  {red}Custom commands are disabled in registry.{end}\n")
                continue

            try:
                convertcustom_Mode = __Command__[1]
                convertcustom_Mode = RemoveStartSpaces(convertcustom_Mode).lower()

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <mode> not found.", "Possible modes: [text/t] - type code inside dsah, [file/f] - convert file to code")
                continue

            if convertcustom_Mode not in ("text", "t", "file", "f"):
                HandleError("soft", __Command__[0], "ArgumentValueError", "Argument value: <mode> is incorrect.", "Possible modes: [text/t] - type code inside dsah, [file/f] - convert file to code")
                continue
            
            if convertcustom_Mode in ("file", "f"):
                try:
                    convertcustom_ModeF_CodePath = RemoveStartSpaces(__Command__[2])
                    if not os.path.exists(convertcustom_ModeF_CodePath):
                        HandleError("soft", __Command__[0], "ArgumentValueError", "Argument: <path> is incorrect.", "That path does not exists.")
                        continue 

                except:
                    HandleError("soft", __Command__[0], "MissingArgument", "Argument: <path> not found.", "Type <path> argument")
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
                        convertcustom_ModeT_CurrentLine = input(f"{gray}{convertcustom_ModeT_LinesCounter}{end}  ")
                        if "<stop>" in convertcustom_ModeT_CurrentLine:
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
                    HandleError("soft", "MissingArgument", "Argument: <code> not fund.", "You have not entered path to code file.", "Enter <code> argument.")
                    continue

        elif __Command__[0] == "cstm.list":
            try:
                print("  Custom commands:")
                for command in _CustomCommandsList_:
                    print(f"    • {command}")
            
                print("\n")

            except:
                HandleError("critical", __Command__[0], "FileError", "Cannot output file content.", "None")


        # Variables
        elif __Command__[0] == "var.list":
            try:
                VarsCP.read(Vars_Path, encoding='utf-8')
                vars_ListOfVariables = VarsCP.sections()
                for name in vars_ListOfVariables:
                    print(f"  {name} = \"{VarsCP[name]['value']}\"")

            except:
                HandleError("critical", __Command__[0], "FileError", "Cannot output file content.", "None")
            
        elif __Command__[0] == "var.add":
            try:
                varadd_Name = __Command__[1]
                varadd_Name = RemoveStartSpaces(varadd_Name).lower()
                
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", "Type <name> argument.")
                continue  

            varadd_ListOfVariables = VarsCP.sections()
            if varadd_Name in varadd_ListOfVariables:
                HandleError("soft", __Command__[0], "ArgumentError", f"Variable named: \"{varadd_Name}\" already exists.", "Edit varaible value or crate new with other name.")
                continue

            try:
                varadd_Value = __Command__[2]
                varadd_Value = RemoveStartSpaces(varadd_Value)

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <value> not found.", "Type <value> argument.")
                continue

            VarsCP[varadd_Name] = {"value": varadd_Value}
            with open(Vars_Path, "w", encoding='utf-8') as f:
                VarsCP.write(f)

        elif __Command__[0] == "var.rem":
            try:
                remvar_Name = __Command__[1]
                remvar_Name = RemoveStartSpaces(remvar_Name).lower()

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", "Type <name> argument.")
                continue  

            VarsCP.read(Vars_Path, encoding='utf-8')
            remvar_ListOfVariables = VarsCP.sections()
            remvar_currentVars = [] 
            for varname in remvar_ListOfVariables:
                remvar_currentVars.append(varname.replace(" ","").lower())
                
            if remvar_Name not in remvar_currentVars:
                HandleError("soft", __Command__[0], "ArgumentError", f"Varaible \"{remvar_Name}\" does not exists", "Type correct argument <name>.")
                continue

            try:
                VarsCP.remove_section(remvar_Name)    
                with open(Vars_Path, "w", encoding='utf-8') as f:
                    VarsCP.write(f)

            except:
                HandleError("critical", __Command__[0], "FileError", "Cannot delete variable.", "None")

        elif __Command__[0] == "var.set":
            try:
                varset_Name = __Command__[1]
                varset_Name = RemoveStartSpaces(varset_Name).lower()

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", "Type <name> argument.")
                continue  

            VarsCP.read(Vars_Path, encoding='utf-8')
            varset_ListOfVariables = VarsCP.sections()
            varset_currentVars = [] 
            for varname in varset_ListOfVariables:
                varset_currentVars.append(varname.replace(" ","").lower())
                
            if varset_Name not in varset_currentVars:
                HandleError("soft", __Command__[0], "ArgumentError", "That variable does't exists.", "Type correct variable name.")
                continue

            try:
                varset_NewValue = RemoveStartSpaces(__Command__[2])

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <value> not found.", "Type <value> argument.")
                continue

            try:
                VarsCP[varset_Name]["value"] = varset_NewValue
                with open(Vars_Path, "w", encoding='utf-8') as f:
                    VarsCP.write(f)

            except:
                HandleError("soft", __Command__[0], "ArgumentError", f"Varaible \"{remvar_Name}\" does not exists", "Type correct argument <name>.")


        # Recovery
        elif __Command__[0] == "rcv.save":
            import files_operations
            files_operations.copy_recovery()
            print(f"  {green}Done.{end}\n")

        elif __Command__[0] == "rcv.restore":
            import files_operations
            files_operations.paste_recovery()
            print(f"  {green}Done.{end}\n")


        # Accounts
        elif __Command__[0] == "acc.create":
            if UserAccount.Permissions != "root":
                HandleError("soft", __Command__[0], "PermissionsError", "Only root can add/modify accounts.", "Repeat process as root.")
                continue

            try:
                acc_create_Name = __Command__[1].replace(" ","")  
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", "Include <name> argument.")
                continue

            try:
                acc_create_Password = RemoveStartSpaces(__Command__[2])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <password> not found.", "Include <password> argument.")
                continue

            try:
                import accounts
            except:
                HandleError("critical", __Command__[0], "ModuleNotFound", "Module: accounts not found.", "Use repair tool to downlaod file online.")
                continue

            try:
                accounts.create(acc_create_Name, bcrypt.hashpw(bytes(acc_create_Password, 'utf-8'), bcrypt.gensalt()))
            except Exception as e:
                HandleError("soft", __Command__[0], "UnexceptedError", e, "None.")

        elif __Command__[0] == "acc.delete":
            if UserAccount.Permissions != "root":
                HandleError("soft", __Command__[0], "PermissionsError", "Only root can add/modify accounts.", "Repeat process as root.")
                continue

            try:
                acc_delete_Name = RemoveStartSpaces(__Command__[1])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", "Include <name> argument.")
                continue

            if acc_delete_Name == "root":
                HandleError("soft", __Command__[0], "PermissionsError", "You don't have permissions to delete [root] account.", "None.")
                continue

            import accounts
            acc_delete_RootPassAccept = accounts.check_root_password()
            if acc_delete_RootPassAccept == False:
                HandleError("soft", __Command__[0], "PermissionsError", "Too much incorrect root passwords tries.", "Try again and write correct password.")
                continue

            try:
                status = accounts.delete(acc_delete_Name)
                if status == True:
                    print(f"  {green}Succesfully removed account.{end}")
                else:
                    HandleError("soft", __Command__[0], "UnexceptedError", f"{status}", "None.")

            except Exception as e:
                HandleError("soft", __Command__[0], "UnexceptedError", f"Error: {e}.", "None.")

        elif __Command__[0] == "acc.chngpasswd":
            if UserAccount.Permissions != "root":
                acc_changepwd_Name = UserAccount.Name.replace(" ","")

            else:
                try:
                    acc_changepwd_Name = __Command__[1].replace(" ","")
                except:
                    HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", "Include <name> argument.")
                    continue
            
            if UserAccount.Permissions != "root":
                try:
                    acc_changepwd_CurrPwd = __Command__[2]

                except:
                    HandleError("soft", __Command__[0], "MissingArgument", "Argument: <current_password> not found.", "Include <current_password> argument.")
                    continue
            else:
                acc_changepwd_CurrPwd = "SKIPPED_BECOUSE_COMMAND_TYPED_BY_ROOT"

            try:
                if acc_changepwd_CurrPwd != "SKIPPED_BECOUSE_COMMAND_TYPED_BY_ROOT":
                    acc_changepwd_NewPwd = RemoveStartSpaces(__Command__[3])
                    
                else:
                    acc_changepwd_NewPwd = RemoveStartSpaces(__Command__[2])

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <new_password> not found.", "Include <new_password> argument.")
                continue


            try:
                import accounts
                status = accounts.change_pass(acc_changepwd_Name, acc_changepwd_CurrPwd, bcrypt.hashpw(bytes(acc_changepwd_NewPwd, 'utf-8'), bcrypt.gensalt()))
                if status == True:
                    print(f"  {green}Succesfully changed password.{end}\n")
                else:
                    HandleError("soft", __Command__[0], "UnexceptedError", status, "None.")
            
            except Exception as e:
                print(e)
                os.system("pause")
                HandleError("critical", __Command__[0], "UnexceptedError", e, "None.")

        elif __Command__[0] == "acc.logout":
            Restart()

        elif __Command__[0] == "acc.rename":
            try:
                acc_rename_CurrName = RemoveStartSpaces(__Command__[1])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <current_name> not found.", "Include <current_name> argument.")
                continue
            
            try:
                acc_rename_NewName = RemoveStartSpaces(__Command__[2])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <new_name> not found.", "Include <new_name> argument.")
                continue

            import accounts
            status = accounts.rename(acc_rename_CurrName, acc_rename_NewName)
            if status == True:
                print(f"  {green}Done.\n{end}")
            else:
                print(f"  {red}{status}{end}")

        elif __Command__[0] == "acc.chngmode":
            if UserAccount.Permissions != "root":
                HandleError("soft", __Command__[0], "PermissionsError", "Only root can add/modify accounts.", "Repeat process as root.")
                continue

            try:
                acc_chngmode_Name = RemoveStartSpaces(__Command__[1])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", "Include <name> argument.")
                continue

            try:
                acc_chngmode_Mode = RemoveStartSpaces(__Command__[2]).lower().replace("root","r").replace("user","u")
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <mode> not found.", "Include <mode> argument.")
                continue
            
            if acc_chngmode_Mode not in ("r","u"):
                HandleError("soft", __Command__[0], "ArgumentError", "Argument: <mode> value is not excepted.", "Specify <mode> by: [root/r] or [user/u].")
                continue

            import accounts
            accounts.change_mode(acc_chngmode_Name, acc_chngmode_Mode)
            print(f"  {green}Done.{end}\n")

        elif __Command__[0] == "acc.list":
            import accounts
            acc_list_Accounts = accounts.list_accounts()
            acc_list_Users = acc_list_Accounts[0]
            acc_list_Roots = acc_list_Accounts[1]

            print("\n")
            for root in acc_list_Roots:
                if root == "root":
                    print(f"  {gray}[r] {blue}|{end} {gray}root{end}")
                else:
                    print(f"  [r] {blue}|{end} {root}")
            print("\n")
            for user in acc_list_Users:
                print(f"  [u] {blue}|{end} {user}")
            print("\n")


        # Other
        elif __Command__[0] == "oscmd":
            ClearOneLine()
            print(f"({_Mode_}) {UserAccount.Name} {blue}{UserAccount.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}{CommandContent}")

            try:
                oscmd_Command = __Command__[1]
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <command> not found.", "Type <command> argument.")
                continue

            try:
                os.system(oscmd_Command)
            except Exception as exc:
                print(f"  {red}Unexcpeted error: {exc}{end}")

        elif __Command__[0] == "viewf":
            try:
                viewf_file_Path = RemoveStartSpaces(__Command__[1])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <file> not found.", "Type <file> argument.")
                continue

            if not os.path.exists(viewf_file_Path):
                if not os.path.exists(viewf_file_Path.replace(" ","")):
                    HandleError("soft", __Command__[0], "ArgumentError", "Path does not exists.", "Type correct <path> argument.")
                    continue

                else:
                    viewf_file_Path = RemoveStartSpaces(viewf_file_Path)

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
                HandleError("soft", __Command__[0], "LocalFileError", "Cannot read file.", "Check if file permissions are great.")
            
        elif __Command__[0] == "checkver":
            detectedUpdate = False
            print(f"  Local version : {_Version_}")
            print("  Checking online version : ",end="")
            git_VersionFile = "https://raw.githubusercontent.com/GentalYT/dash/main/version"
            git_Request = requests.get(git_VersionFile).text.replace("\n","")
            if _Version_ != git_Request:
                try:
                    git_Request = int(git_Request)
                    
                except:
                    print("VersionFile.NonInt - Cannot check.\n")
                    continue

                if git_Request > _Version_:
                    detectedUpdate = True  
                    print(f"{orange}Detected Update! [{git_Request}]{end}\n")

                else:
                    print(f"{green}You are up to date. [{git_Request}]{end}\n")
                    
            else:
                print(f"{green}You are up to date. [{git_Request}]{end}\n")

        elif __Command__[0] == "checkfiles":
            try:
                print("    ",end="")
                files_operations.check()
                print(f"  \n{green}    Done.\n{end}")

            except Exception as exc:
                HandleError("critical", __Command__[0], exc, "Error while trying to check files.", "None")
        
        elif __Command__[0] == "help.commands":
            try:
                import files_operations
                files_operations.help_commands()
            except:
                HandleError("soft", __Command__[0], "FileError", "Cannot display commands list.", "None")

        elif __Command__[0] == "debg.exe":
            if UserAccount.Permissions != "root":
                HandleError("soft", __Command__[0], "PermissionsError", "Only root can use debugger.", "Repeat process as root.")
                continue

            try:
                exec(RemoveStartSpaces(__Command__[1]))
                print(f"  {green}Done.{end}\n")

            except Exception as e:
                print(f"  {red}Error:{end} {e}\n")  
     
        else:
            ClearOneLine()
            print(f"[{_Mode_}] {UserAccount.Name} {red}{UserAccount.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}{CommandContent}")


except Exception as e:
    try:
        import critical_mode
        critical_mode.CriticalMode("Unexcepted error. - "+str(e))

    except Exception as e:
        Cls()
        print("   MAJOR ERROR. \"Critical Mode\" not found. Preparing to autorepair")
        print("\n\n  [*] Restore user files.  :  ",end="")

        try:
            import files_operations
            files_operations.paste_recovery()
            print("(Done) - Done.")

        except Exception as e:
            print(f"(Error) - {e}")


        print("  [*] Install libaries.  :  ",end="") 
        try:
            import install_libaries
            install_libaries.InstallRequiredPackages()
            print("(Done) - Done.")
        
        except Exception as e:
            print(f"(Error) - {e}")
        

        print("  [*] Download code files.  :  ",end="")
        try:
            import update_code
            print("(Done) - Done.")
        
        except Exception as e:
            print(f"(Error) - {e}")

