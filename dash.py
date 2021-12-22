_Version_ = 6

try:

    # Import packages
    print("  [Info] Importing packages: ", end="")
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

    Vars_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\vars.dash"
    Config_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\config.dash"
    Registry_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\reg.dash"
    MainFolder_Path = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\"
    Commands_Path     = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\commands.dash"
    print("OK")


    # Check files health
    print("  [Info] Checking files <", end="")
    import files_operations
    files_operations.check()
    print("> : OK")


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
    def RemoveStartSpaces(text):
        listed = list(text)
        for i, char in enumerate(listed):
            if char == " ":
                listed.pop(i)
        
        return ListToString(listed)


    # showbootupinfo entry barrier
    RegistryCP.read(Registry_Path)
    if RegistryCP["reg"]["showBootupInfo"] == "true":
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

        # Set mode
        if isAdmin() == True:
            if RegistryCP["reg"]["modeasemote"] == "true":
                _Mode_ = "🔧"
            else:
                _Mode_ = "root"            
        else:
            if RegistryCP["reg"]["modeasemote"] == "true":
                _Mode_ = "👤"
            else:
                _Mode_ = "nrml"

        # Colors
        end    =  "\033[0m"
        red    =  "\033[1;31m"
        gray   =  "\033[1;30m"
        blue   =  "\033[1;34m"
        green  =  "\033[1;32m"
        orange =  "\033[1;33m"
        TurnColors()

        # Main input
        __Command__ = input(f"[{_Mode_}] {UserConfig.Name} {gray}{UserConfig.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}")
        CommandContent = __Command__
        __Command__ = FormatInput(__Command__)

        # Good command
        ClearOneLine()
        print(f"[{_Mode_}] {UserConfig.Name} {green}{UserConfig.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}{CommandContent}")


        if __Command__[0]   == "exit":
            exit()

        elif __Command__[0] == "restart":
            os.system("py dash.py")
            Cls()
            exit()

        elif __Command__[0] == "cls":
            Cls()

        elif __Command__[0] == "devtest":
            print("  •")
            # for el in __Command__:
            #     print(el)
            

        # Settings
        elif __Command__[0] == "mycfg":
            try:
                print(f"  Name      ==  \"{UserConfig.Name}\"")
                print(f"  Cursor    ==  \"{UserConfig.Cursor}\"")
                print(f"  Sepchar   ==  \"{UserConfig.Sepchar}\"")
                print(f"  Oschar    ==  \"{UserConfig.OsChar}\"\n")

            except Exception as exc:
                HandleError("critical", __Command__[0], exc, "Cannot read user configuration", "None")

        elif __Command__[0] == "set.name":
            try:
                setname_NewName = RemoveStartSpaces(__Command__[1])

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", f"After command, type sepchar (current: \"{UserConfig.Sepchar}\") and your new username")
                continue

            if setname_NewName.replace(" ", "") == "":
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <name> not found.", f"After command, type sepchar (current: \"{UserConfig.Sepchar}\") and your new username")
                continue

            if RegistryCP["reg"]["checkArgLenght"] == "true":
                if len(setname_NewName) > 31:
                    HandleError("soft", __Command__[0], "ArgumentLenghtError", "Argument: <name> is too long.", "Your name cannot be longer than 30 characters. You can turn off this setting in registry.")
                    continue

            try:
                ConfigCP["customization"]["name"] = setname_NewName
                with open(Config_Path, "w", encoding='utf-8') as f:
                    ConfigCP.write(f)

            except Exception as exc:
                HandleError("critical", __Command__[0], exc, "Cannot write to file.", "None")

        elif __Command__[0] == "set.cursor":
            try:
                setcursor_NewCursor = RemoveStartSpaces(__Command__[1])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <cursor> not found.", f"After command, type sepchar (current: \"{UserConfig.Sepchar}\") and your new cursor")
                continue

            if setcursor_NewCursor.replace(" ", "") == "":
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <cursor> not found.", f"After command, type sepchar (current: \"{UserConfig.Sepchar}\") and your new cursor")
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
                setsepchar_NewChar = RemoveStartSpaces(__Command__[1])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <sepchar> not found", f"After command, type sepchar (current: \"{UserConfig.Sepchar}\") and your new sepchar")
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
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <setoschar> not found", f"After command, type sepchar (current: \"{UserConfig.Sepchar}\") and your new setoschar")
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
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <target> not found", f"After command, type sepchar (current: \"{UserConfig.Sepchar}\") and target ip.")
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
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <target> not found", f"After command, type sepchar (current: \"{UserConfig.Sepchar}\") and target ip.")
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

                print("  ==== REGSHOW ====\n")
                for i, entry in enumerate(RegistryEntries):
                    print(f"  [{i+1}] |  {green+'T' if entry[1] == 'true' else red+'F'}{end} {entry[0]}")

                print("\n")

            except Exception as exc:
                HandleError("critical", __Command__[0], "LoadingRegInfoError", f"Exception: {exc}", "None")

        elif __Command__[0] == "dreg.edit":

            try:
                dregedit_EntryName = RemoveStartSpaces(__Command__[1])
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <entry.name> not found.", "Type argument: <entry.name>")
                continue

            try:
                dregedit_NewValue = RemoveStartSpaces(__Command__[2])

            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <entry.value> not found.", "Type argument: <entry.value>")
                continue

            dregedit_StableEntriesList = RegistryCP.items("reg")
            dregedit_ListOfEntries = [entry[0] for entry in dregedit_StableEntriesList]
            
            dregedit_EntryName = dregedit_EntryName.replace(" ", "")
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

                print(f"  {green}Your registry code:{end} {''.join(dregedit_OutputList)}", end="")
                if RegistryCP["reg"]["copyoutput"] == "true":
                    pyperclip.copy(''.join(dregedit_OutputList))
                    print(f"  {gray}(copied.){end}")

                print("\n")

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

                print("\n")

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
            files_operations.copy_recovery()
            print(f"{green}Done.{end}")

        elif __Command__[0] == "rcv.restore":
            files_operations.paste_recovery()
            print(f"{green}Done.{end}")


        # Other
        elif __Command__[0] == "oscmd":
            ClearOneLine()
            print(f"({_Mode_}) {UserConfig.Name} {blue}{UserConfig.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}{CommandContent}")

            try:
                oscmd_Command = __Command__[1]
            except:
                HandleError("soft", __Command__[0], "MissingArgument", "Argument: <command> not found.", "Type <command> argument.")
                continue

            try:
                os.system(oscmd_Command)
            except Exception as exc:
                print(f"  {red}Unexcpeted error: {exc}{end}")

        elif __Command__[0] == "root":
            # try:
            #     pyuac.runAsAdmin()
            # except:
            #     print(f"  {red}Cannot run Dash with administrator permissions.{end}")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

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
        
        else:
            ClearOneLine()
            print(f"[{_Mode_}] {UserConfig.Name} {red}{UserConfig.Cursor}{end}{' ' if RegistryCP['reg']['spaceAfterCursor'] == 'true' else ''}{CommandContent}")
    
except Exception as e:
    try:
        import critical_mode
        critical_mode.CriticalMode("Unexcepted error. - "+str(e))
        exit()

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


