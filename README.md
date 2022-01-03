# Dash Console.
~ Small project to make terminal usage easier. Work's only on Windows.


## Author

- [@gental-py](https://www.github.com/gental-py)


## Features
- Easy to use.
- Full customization.
- Custom commands.
- Custom separator.
- Easy and clear interface.
- Lot of commands


## Files localization:
#### `Main folder` - `C:\Users\USERNAME\Appdata\Local\.dash\`
#### `Users` - `C:\Users\USERNAME\Appdata\Local\.dash\users\`
#### `Backup` - `C:\Users\USERNAME\Appdata\LocalLow\.dash_recovery\`
#### `Modules` - `.\ (Same as dash.py)`


## What is `sepchar`?
Sepchar is character that will separate arguments. Deafult = `,`. Example: `var.add , Age , 21` 


## Commands
| Command                        | Effect                                     |
|--------------------------------|--------------------------------------------|
|     **Basics**                 |                                            |
| `exit`                         | Exit program.                              |
| `restart`                      | Restart program.                           |
| `cls`                          | Clear screen.                              |
|     **Config**                 |                                            |
| `mycfg`                        | Display current config.                    |
| `set.cursor <cursor>`          | Set new cursor.                            |
| `set.sepchar <sepchar>`        | Set new sepchar.                           |
| `set.oschar <oschar>`          | Set new system command prefix.             |
|     **Network**                |                                            |
| `netinfo`                      | Display your network info.                 |
| `dnslkp <target.addr>`         | Dns lookup an addres.                      |
| `revdnslkp <target.ip>`        | Reversed DNS lookup. (ip->addr)            |
| `ipgeoinfo <target.ip>`        | Returns ip geo location. (Country, city)   |
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
|     **Accounts (as root)**     |                                            |
| `acc.create <name> <pass>`     | Create account.                            |
| `acc.delete <name>`            | Delete account.                            |
| `acc.chngpasswd <name> <pass>` | Change an account password.                |
| `acc.logout`                   | Brings you back to login screen.           |
| `acc.rename <name> <newname>`  | Rename an account.                         |
| `acc.chngmode <name> <mode>`   | Change an account mode. <root/user>        |
| `acc.list`                     | Shows list of all accounts.                |
|     **Accounts (as user)**     |                                            |
| `acc.chngpasswd <pass> <new>`  | Change current account password.           |
| `acc.logout`                   | Brings you back to login screen.           |
| `acc.rename <newname>`         | Change current account name.               |
| `acc.list`                     | Show list of all accounts.                 |
|     **Other**                  |                                            |
| `root`                         | Try to open Dash with root permisions.     |
| `viewf <path>`                 | Display file with simple highlithing.      |
| `checkver`                     | Shows local version and check for updates. |
| `checkfiles`                   | Check program files health.                |


## Registry (dreg)
| Index | Entry                          | Effect                                          | Deafult |
|-------|--------------------------------|-------------------------------------------------|---------|
|   1   | `loginNameAsNumber`            | Shows names and their index and ask for index.  |    F    |
|   2   | `checkArgLenght`               | Checks arguments lenght.                        |    T    |
|   3   | `spaceAfterCursor`             | Add's space after cursor. T/F: (> text) (>text) |    T    |
|   4   | `enableColors`                 | Turn on colors. (Recomended for easier usage)   |    T    |
|   5   | `copyOutput`                   | Automaticly copying some commands output.       |    F    |
|   6   | `showBootupInfo`               | Requires to press any key after read boot logs. |    F    |
|   7   | `enableCustomCommands`         | Enables custom commands.                        |    T    |
|   8   | `advancedErrorOutput`          | Show more informations about errors. (Advanced) |    F    |
|   9   | `autoUpdate`                   | Automaticly install updates when detected.      |    F    |


## Accounts
Every account have own: custom commands, custom variables, config and `account` file.

Account can have: `root` or `user` permissions.
`Root`:
Can do everything excepting editing `[root]` account. (Deafult account) 

`User`:
Have limited permissions. Cannot edit dregistry, manage other account. (Can change name and password for their own)
Can manage their config and custom files.

Passwords security:
All passwords are encrypted and hashed using `bcrypt` module. Password cannot be decoded to string, but can be brute-forced.
