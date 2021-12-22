# Dash Console.
~ Small project to make terminal usage easier. Work's on Windows, but can be runned on other systems. 


## Author

- [@gentalyt](https://www.github.com/gentalyt)


## Features
- Easy to use.
- Full customization.
- Custom commands.
- Custom separator.
- Easy and clear interface.
- Lot of commands


## What is `sepchar`?
Sepchar is character that will separate arguments. Deafult = `!`. Example: `var.add ! Age ! 21` 


## Commands
| Command                        | Effect                                     | 
|--------------------------------|--------------------------------------------|
|     **Basics**                 |                                            |
| `exit`                         | Exit program.                              |
| `restart`                      | Restart program.                           |
| `cls`                          | Clear screen.                              | 
|     **Config**                 |                                            |
| `mycfg`                        | Display current config.                    |
| `set.name <name>`              | Set new name.                              |
| `set.cursor <cursor>`          | Set new cursor.                            |
| `set.sepchar <sepchar>`        | Set new sepchar.                           |
| `set.oschar <oschar>`          | Set new system command prefix.             |    
|     **Network**                |                                            |
| `netinfo`                      | Display your network info.                 |
| `dnslkp <target.addr>`         | Dns lookup an addres.                      |
| `revdnslkp <target.ip>`        | Reversed DNS lookup. (ip->addr)            |
|     **Dash Registry**          |                                            |
| `dreg.show`                    | Show entries and values.                   |
| `dreg.edit <entry> <value>`    | Change entry value. [true/false]           |
| `dreg.copy`                    | Copy current registry code.                |
| `dreg.paste <code>`            | Paste registry code.                       | 
| `dreg.reset`                   | Reset registry.                            |
|     **Custom Commands**        |                                            |
| `<custom.name>`                | Execute custom command.                    |
| `cstm.add <name>`              | Create custom command.                     |
| `cstm.open`                    | Open custom commands file.                 |
| `cstm.convert <mode> <%path>`  | Convert py script to dash. <text/file>     |
| `cstm.list`                    | Lists all custom commands.                 |
|     **Variables**              |                                            |
| `var.list`                     | Lists all variables and their values.      |
| `var.add <name> <value>`       | Create variable and assign value.          |
| `var.rem <name>`               | Remove variable.                           |
| `var.set <name> <value>`       | Assign new value for variable.             |
|     **Recovery**               |                                            |
| `rcv.save`                     | Save current user files image.             |
| `rcv.restore`                  | Restore saved files.                       |
|     **Other**                  |                                            |
| `root`                         | Try to open Dash with root permisions.     |
| `viewf <path>`                 | Display file with simple highlithing.      |                        
| `checkver`				             | Shows local version and check for updates. |
| `checkfiles`                   | Check program files health.                |



## Files
#### `Main folder` - `C:\Users\USERNAME\Appdata\Local\.dash\`
Folder, where all other files are stored.
#### `Config` - `C:\Users\USERNAME\Appdata\Local\.dash\config.dash`
User configuration file.
#### `Registry` - `C:\Users\USERNAME\Appdata\Local\.dash\reg.dash`
Program configuration file.
#### `Custom commands` - `C:\Users\USERNAME\Appdata\Local\.dash\commands.dash`
Custom commands, that you can use in terminal.


