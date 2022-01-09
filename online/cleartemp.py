#< Module to clear temporary files. ># 


import os, ctypes, time
ppl = "\033[1;35m" # text
red = "\033[1;31m" # errors
grn = "\033[1;32m" # succes
end = "\033[0m"    # end


def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


if not isAdmin():
    print(f"{red}[!] Warning: Script is not running as admin. It will delete less files.\nDo you want to continue? y/n{end}")
    askforcont = input("[Y/N] >").lower()
    while askforcont not in ("y", "n"):
        askforcont = input("[Y/N] >").lower()

    if askforcont == "n":
        print(end)
        exit()

tmpfile_errors = 0
tmpfile_succes = 0
tmpfile_count  = 0

for root, dirs, files in os.walk("C:\\"):
    for file in files:
        if file.endswith(".tmp"):
            tmp_file_path = os.path.join(root, file)
            tmpfile_count += 1
            try:
                os.remove(tmp_file_path)
                print(f"{grn}[{tmpfile_count}] Deleted .tmp file: \"{tmp_file_path}\"{end}")
                tmpfile_succes += 1

            except:
                print(f"{red}[{tmpfile_count}] Error: cannot delete .tmp file: \"{tmp_file_path}\" {end}")
                tmpfile_errors += 1

print("\n" * 5)
print(f"{end}Ended deleting .tmp files process.")
print(f"{end}Status:  {ppl}Total: {tmpfile_count}  {ppl} |  {grn}Succes: {tmpfile_succes}  {ppl} |  {red} Errors: {tmpfile_errors} {end}")
print("\n" * 5)

time.sleep(2.5)

folderfile_count = 0
folder_succes = 0
folder_errors = 0

temp_folder_path = "C:\\Users\\win83\\AppData\\Local\\Temp\\"
for root, dirs, files in os.walk(temp_folder_path):
    for file in files:
        folder_file_path = os.path.join(root, file)
        folderfile_count += 1
        try:
            os.remove(folder_file_path)
            print(f"{grn}[{tmpfile_count}] Deleted file: \"{folder_file_path}\"{end}")
            folder_succes += 1

        except:
            print(f"{red}[{tmpfile_count}] Error: cannot delete file: \"{folder_file_path}\" {end}")
            folder_errors += 1


print("\n" * 5)
print(f"{end}Ended deleting TEMP folder files.")
print(f"{end}Status:  {ppl}Total: {folderfile_count}  {ppl} |  {grn}Succes: {folder_succes}  {ppl} |  {red} Errors: {folder_errors} {end}")
print("\n" * 5)

dirs  = [f for f in os.listdir(temp_folder_path) if not os.path.isfile(os.path.join(temp_folder_path, f))]
dir_succes = 0
dir_errors = 0
for dir in dirs:
    try:
        os.rmdir(temp_folder_path+dir)
        print(f"{grn}[{tmpfile_count}] Deleted folder: \"{folder_file_path}\{dir}\"{end}")
        dir_succes += 1

    except:
        print(f"{red}[{tmpfile_count}] Cannot delete folder: \"{folder_file_path}\{dir}\"{end}")
        dir_errors += 1

print("\n" * 5)
print(f"{end}Ended deleting folders.")
print(f"{end}Status:  {ppl}Total: {dir_errors+dir_succes}  {ppl} |  {grn}Succes: {dir_succes}  {ppl} |  {red} Errors: {dir_errors} {end}")
print("\n" * 5)
