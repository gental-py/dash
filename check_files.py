def check():
    import os, getpass

    try:
        import configparser as cp

    except:
        try:
            os.system("pip install configparser")
            import configparser as cp

        except:
            print("  CriticalError: Cannot import configparser.")
            exit()

    def RegenerateFile(loc):
        os.remove(loc)
        open(loc, "a+")

    _OsUsername_ = getpass.getuser()

    VarsCP = cp.ConfigParser()
    ConfigCP = cp.ConfigParser()
    RegistryCP = cp.ConfigParser()
    CommandsCP   = cp.ConfigParser()

    Vars_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\vars.dash"
    Config_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\config.dash"
    Registry_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\reg.dash"
    MainFolder_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\"
    Commands_Loc     = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\commands.dash"

    # Does files exists?

    # Main folder
    if not os.path.exists(MainFolder_Loc):
        print("_mainfolder.notexisting_",end="")
        os.mkdir(MainFolder_Loc)

    # Vars
    if not os.path.exists(Vars_Loc):
        print("_vars.notexisting_",end="")
        open(Vars_Loc, "a+").close()

    # Commands
    if not os.path.exists(Commands_Loc):
        print("_commands.notexisting_",end="")
        open(Commands_Loc, "a+").close()

    # Registry
    if not os.path.exists(Registry_Loc) or os.path.getsize(Registry_Loc) == 0:
        print("_registry.notexisting_",end="")
        open(Registry_Loc, "a+").close()
        RegistryCP["reg"] = {"checkArgLenght": "true", "spaceAfterCursor": "true", "enableColors": "true", "copyOutput": "false", "showBootupInfo": "false", "enableCustomCommands": "true", "advancedErrorOutput": "false"}
        with open(Registry_Loc, "w") as file:
            RegistryCP.write(file)

    # Config
    if not os.path.exists(Config_Loc) or os.path.getsize(Config_Loc) == 0:
        print("_config.notexisting_",end="")
        open(Config_Loc, "a+").close()
        ConfigCP["customization"] = {"name": _OsUsername_, "cursor": "•", "sepchar": ",", "oschar": "."}
        with open(Config_Loc, "w") as file:
            ConfigCP.write(file)


    # Is files data health great?

    # vars.dash
    try:
        VarsCP.read(Vars_Loc)
        listOfVariables = VarsCP.sections()
        for Varname in listOfVariables:
            try:
                var = VarsCP[Varname]["value"]
        
            except:
                print(f"_vars.incorrectvalue_",end="")
                vars_open_R = open(Vars_Loc, "r", encoding="utf-8")
                var_Content = vars_open_R.read()
                vars_open_R.close()
                var_Content = var_Content.replace(f"[{Varname}]", "")
                vars_open_Wp = open(Vars_Loc, "w+", encoding="utf-8")
                vars_open_Wp.write(var_Content)
                vars_open_Wp.close()   
    except:
        print("_regen.vars_",end="")
        RegenerateFile(Vars_Loc)

    # commands.dash
    try:
        CommandsCP.read(Commands_Loc)
        listOfCommands = CommandsCP.sections()
        for CommandName in listOfCommands:
            try:
                comm = CommandsCP[CommandName]["value"]

            except:
                print(f"_commands.incorrectvalue_",end="")
                cmd_open_R = open(Commands_Loc, "r", encoding="utf-8")
                cmd_Content = cmd_open_R.read()
                cmd_open_R.close()
                cmd_Content = cmd_Content.replace(f"[{CommandName}]", "")
                cmd_open_Wp = open(Commands_Loc, "w+", encoding="utf-8")
                cmd_open_Wp.write(cmd_Content)
                cmd_open_Wp.close()              
    except: 
        print("_regen.commands_",end="")
        RegenerateFile(Commands_Loc)

    # reg.dash
    try:
        EntriesList = ["modeasemote", "advancederroroutput", "checkarglenght", "spaceaftercursor", "enablecolors", "copyoutput", "showbootupinfo", "enablecustomcommands"]

        RegistryCP.read(Registry_Loc)
        RegEntries = RegistryCP.items("reg")

        # Checking entries values
        for Entry in RegEntries:

            # Check if entry value is true or false
            if Entry[1] != "true" and Entry[1] != "false":
                print("_registry.nonbooleanvalue_",end="")
                RegistryCP["reg"][Entry[0]] = "false"
                with open(Registry_Loc, "w") as f:
                    RegistryCP.write(f)

            # Check for invalid entry
            if Entry[0] not in EntriesList:
                print(f"_registry.unxcptentry_",end="")
                RegistryCP.remove_option("reg", Entry[0])
                with open(Registry_Loc, "w") as f:
                    RegistryCP.write(f)

        # Check for missing entry
        EntriesNamesList = [RegEntries[x][0] for x in range(len(RegEntries))]
        for mainEntryName in EntriesList:
            if mainEntryName not in EntriesNamesList:
                print(f"_registry.missingentry_",end="")
                RegistryCP["reg"][mainEntryName] = "false"
                with open(Registry_Loc, "w") as f:
                    RegistryCP.write(f)
    except:
        print("_regen.registry_",end="")
        RegenerateFile(Registry_Loc)
        RegistryCP["reg"] = {"modeAsEmote": "false", "checkArgLenght": "true", "spaceAfterCursor": "true", "enableColors": "true", "copyOutput": "false", "showBootupInfo": "false", "enablecustomcommands": "true", "advancedErrorOutput": "false"}
        with open(Registry_Loc, "w") as file:
            RegistryCP.write(file)

    # config.dash
    try:
        ConfigNames = ["name", "cursor", "sepchar", "oschar"]

        ConfigCP.read(Config_Loc, encoding="utf-8")
        CfgItems = ConfigCP.items("customization")

        # Check values
        for Setting in CfgItems:

            # Check for unexcepted settings
            if Setting[0] not in ConfigNames:
                print("_config.unxcptentry_",end="")
                ConfigCP.remove_option("customization", Setting[0])
                with open(Config_Loc, "w") as f:
                    ConfigCP.write(f)
            
            # Check for invalid settings values
            try:
                sttng = Setting[1]
                if Setting[1].replace(" ","") == "":
                    print("_config.wrongvalue_",end="")
                    ConfigCP["customization"][Setting[0]] = "!R"
                    with open(Config_Loc, "w") as f:
                        ConfigCP.write(f)
            except:
                print("_config.wrongvalue_",end="")
                ConfigCP["customization"][Setting[0]] = "!R"
                with open(Config_Loc, "w") as f:
                    ConfigCP.write(f)
            
        # Check for missing settings
        ConfigOptions = [CfgItems[x][0] for x in range(len(CfgItems))]
        for mainOption in ConfigNames:
            if mainOption not in ConfigOptions:
                print("_config.missingsetting_",end="")
                ConfigCP["customization"][mainOption] = "!G"
                with open(Config_Loc, "w") as f:
                    ConfigCP.write(f)
    except:
        print("_regen.config_",end="")
        RegenerateFile(Config_Loc)
        ConfigCP["customization"] = {"name": _OsUsername_, "cursor": "•", "sepchar": ",", "oschar": "."}
        with open(Config_Loc, "w") as file:
            ConfigCP.write(file)

            
    print(" | Validation: check_files.py",end="")
