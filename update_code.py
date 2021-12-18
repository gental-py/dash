import os

try:
    import requests

except:
    try:
        os.system("pip install requests")
        import requests
    except:
        print("  Cannot import requests.")
        exit()

scriptRootURL = r"https://raw.githubusercontent.com/GentalYT/dash/main/"
cfg = ["dash.py", "check_files.py", "critical_mode.py", "install_libaries.py"]

for name in cfg:
    with open(name, "w", encoding="utf-8") as f:
        f.write(requests.get(scriptRootURL + name).text.replace("\n",""))

print("  Installed update.")
import dash