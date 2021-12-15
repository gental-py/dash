Version=0.4


# Dash Console.

Small project to make terminal usage easier. Work's on Windows, but can be runned on other systems. 


## Author

- [@gentalyt](https://www.github.com/gentalyt)


## Features

- Easy to use.
- Full customization.
- Custom commands.
- Custom separator.
- Easy and clear interface.



## Installation

1.
Download and run `dash.py`. Other files will be automaticly generated.

2.
```bash
  npm install dash
  cd dash
  py dash.py
```
    
## What is `sepchar`?
Sepchar is character that will separate arguments. Deafult = `.`. You can test it by typing: `testarg . an argument . second arg` etc.

## How to use configuration?

- `mycfg` - Show your current config
- `setname <name>` - Set new name
- `setcursor <cursor>` - Set new cursor
- `setsepchar <sepchar>` - Set new sepchar. Use `_` as argument separator to replace it with space.
- `setoschar <char>` - Set character that have to be command prefix to execute command by CMD.

## How to use registry?
- `dregshow` - Show your current registry settings.
- `dregedit <entryname> <f/false/0 or t/true/1>` - Change entry value
- `dregcopy` - Copy your settings as code
- `dregpaste` - Paste settings
- `dregreset` - Reset registry to deafult.

## How to use variables?
- `vars` - Show variables and values
- `varadd <name> <value>` - Create variable
- `remvar <name>` - Remove variable
- `varset <name> <NewValue>` - Set variable value
If you want to enter variable, type `${name}`

## Files
#### `Main folder` - `C:\Users\USERNAME\Appdata\Local\.dash\`
Folder, where all other files are stored.
#### `Config` - `C:\Users\USERNAME\Appdata\Local\.dash\config.dash`
User configuration file.
#### `Registry` - `C:\Users\USERNAME\Appdata\Local\.dash\reg.dash`
Program configuration file.
#### `Custom commands` - `C:\Users\USERNAME\Appdata\Local\.dash\commands.dash`
Custom commands, that you can use in terminal.


